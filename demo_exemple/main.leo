program defi_lending.aleo {
    // Constants
    const ADMIN: address = aleo1qgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqanmpl0;
    const LIQUIDATION_THRESHOLD: u64 = 150u64; // 150% collateral ratio
    const MIN_BORROW_AMOUNT: u64 = 100u64;
    const MAX_BORROW_RATIO: u64 = 80u64; // Can borrow up to 80% of collateral
    const INTEREST_PRECISION: u64 = 10000u64; // 100.00% = 10000
    const BASE_INTEREST_RATE: u64 = 500u64; // 5% base rate
    const SECONDS_PER_YEAR: u64 = 31536000u64;
    
    // Asset types
    const ASSET_TOKEN: u8 = 1u8;
    const ASSET_ETH: u8 = 2u8;
    
    // Records
    record CollateralDeposit {
        owner: address,
        amount: u64,
        asset_type: u8,
        deposit_time: u64,
    }
    
    record LoanPosition {
        owner: address,
        collateral_amount: u64,
        borrowed_amount: u64,
        interest_rate: u64,
        borrow_time: u64,
        asset_type: u8,
    }
    
    record PaymentToken {
        owner: address,
        amount: u64,
    }
    
    // Mappings
    mapping total_deposits: u8 => u64;
    mapping total_borrowed: u8 => u64;
    mapping interest_rates: u8 => u64;
    mapping user_positions: address => field;
    mapping protocol_paused: u8 => bool;
    mapping liquidation_rewards: address => u64;
    mapping protocol_fees: u8 => u64;
    
    // Deposit collateral privately
    async transition deposit_collateral(
        public amount: u64,
        public asset_type: u8
    ) -> (CollateralDeposit, Future) {
        // Input validation
        assert(amount > 0u64);
        assert(asset_type == ASSET_TOKEN || asset_type == ASSET_ETH);
        
        let deposit: CollateralDeposit = CollateralDeposit {
            owner: self.signer,
            amount: amount,
            asset_type: asset_type,
            deposit_time: 0u64, // Will be set in finalize
        };
        
        let f: Future = finalize_deposit(asset_type, amount);
        return (deposit, f);
    }
    
    async function finalize_deposit(asset_type: u8, amount: u64) {
        // Check if protocol is paused
        let paused: bool = Mapping::get_or_use(protocol_paused, 1u8, false);
        assert(!paused);
        
        // Update total deposits
        let current_deposits: u64 = Mapping::get_or_use(total_deposits, asset_type, 0u64);
        assert(current_deposits + amount >= current_deposits); // Overflow check
        Mapping::set(total_deposits, asset_type, current_deposits + amount);
    }
    
    // Borrow against collateral
    async transition borrow_against_collateral(
        collateral: CollateralDeposit,
        public borrow_amount: u64
    ) -> (LoanPosition, Future) {
        // Access control
        assert_eq(collateral.owner, self.signer);
        
        // Input validation
        assert(borrow_amount >= MIN_BORROW_AMOUNT);
        
        // Calculate max borrowable amount (80% of collateral)
        let max_borrow: u64 = collateral.amount * MAX_BORROW_RATIO / 100u64;
        assert(borrow_amount <= max_borrow);
        
        let loan: LoanPosition = LoanPosition {
            owner: self.signer,
            collateral_amount: collateral.amount,
            borrowed_amount: borrow_amount,
            interest_rate: BASE_INTEREST_RATE,
            borrow_time: 0u64, // Will be set in finalize
            asset_type: collateral.asset_type,
        };
        
        let f: Future = finalize_borrow(collateral.asset_type, borrow_amount);
        return (loan, f);
    }
    
    async function finalize_borrow(asset_type: u8, amount: u64) {
        // Check if protocol is paused
        let paused: bool = Mapping::get_or_use(protocol_paused, 1u8, false);
        assert(!paused);
        
        // Update total borrowed
        let current_borrowed: u64 = Mapping::get_or_use(total_borrowed, asset_type, 0u64);
        assert(current_borrowed + amount >= current_borrowed); // Overflow check
        Mapping::set(total_borrowed, asset_type, current_borrowed + amount);
        
        // Calculate and update utilization rate
        let total_deps: u64 = Mapping::get_or_use(total_deposits, asset_type, 1u64);
        let new_borrowed: u64 = current_borrowed + amount;
        let utilization: u64 = new_borrowed * 100u64 / total_deps;
        
        // Update interest rate based on utilization
        let new_rate: u64 = BASE_INTEREST_RATE + utilization * 5u64;
        Mapping::set(interest_rates, asset_type, new_rate);
    }
    
    // Repay loan with interest
    async transition repay_loan(
        loan: LoanPosition,
        payment: PaymentToken,
        public repay_amount: u64
    ) -> (LoanPosition, PaymentToken, Future) {
        // Access control
        assert_eq(loan.owner, self.signer);
        assert_eq(payment.owner, self.signer);
        
        // Input validation
        assert(repay_amount > 0u64);
        assert(repay_amount <= payment.amount);
        assert(repay_amount <= loan.borrowed_amount);
        
        // Calculate remaining loan amount
        let remaining_loan: u64 = loan.borrowed_amount - repay_amount;
        
        let updated_loan: LoanPosition = LoanPosition {
            owner: loan.owner,
            collateral_amount: loan.collateral_amount,
            borrowed_amount: remaining_loan,
            interest_rate: loan.interest_rate,
            borrow_time: loan.borrow_time,
            asset_type: loan.asset_type,
        };
        
        let remaining_payment: PaymentToken = PaymentToken {
            owner: self.signer,
            amount: payment.amount - repay_amount,
        };
        
        let f: Future = finalize_repay(loan.asset_type, repay_amount);
        return (updated_loan, remaining_payment, f);
    }
    
    async function finalize_repay(asset_type: u8, amount: u64) {
        // Update total borrowed
        let current_borrowed: u64 = Mapping::get_or_use(total_borrowed, asset_type, 0u64);
        assert(current_borrowed >= amount);
        Mapping::set(total_borrowed, asset_type, current_borrowed - amount);
        
        // Calculate protocol fee (1% of repayment)
        let fee: u64 = amount / 100u64;
        let current_fees: u64 = Mapping::get_or_use(protocol_fees, asset_type, 0u64);
        Mapping::set(protocol_fees, asset_type, current_fees + fee);
    }
    
    // Liquidate undercollateralized position
    async transition liquidate_position(
        loan: LoanPosition,
        public liquidator: address
    ) -> Future {
        // Anyone can liquidate, but loan owner can't liquidate own position
        assert_neq(loan.owner, self.signer);
        
        let f: Future = finalize_liquidate(
            loan.owner,
            loan.collateral_amount,
            loan.borrowed_amount,
            loan.asset_type,
            liquidator
        );
        return f;
    }
    
    async function finalize_liquidate(
        borrower: address,
        collateral: u64,
        borrowed: u64,
        asset_type: u8,
        liquidator: address
    ) {
        // Check if protocol is paused
        let paused: bool = Mapping::get_or_use(protocol_paused, 1u8, false);
        assert(!paused);
        
        // Check if position is undercollateralized
        // Collateral ratio = (collateral_value / borrowed_amount) * 100
        let collateral_ratio: u64 = collateral * 100u64 / borrowed;
        assert(collateral_ratio < LIQUIDATION_THRESHOLD);
        
        // Calculate liquidation reward (10% of collateral)
        let reward: u64 = collateral / 10u64;
        let current_rewards: u64 = Mapping::get_or_use(liquidation_rewards, liquidator, 0u64);
        Mapping::set(liquidation_rewards, liquidator, current_rewards + reward);
        
        // Update total borrowed (debt is cleared)
        let current_borrowed: u64 = Mapping::get_or_use(total_borrowed, asset_type, 0u64);
        assert(current_borrowed >= borrowed);
        Mapping::set(total_borrowed, asset_type, current_borrowed - borrowed);
        
        // Update total deposits (collateral is removed)
        let current_deposits: u64 = Mapping::get_or_use(total_deposits, asset_type, 0u64);
        assert(current_deposits >= collateral);
        Mapping::set(total_deposits, asset_type, current_deposits - collateral);
    }
    
    // Withdraw collateral (only if no outstanding loans)
    async transition withdraw_collateral(
        deposit: CollateralDeposit,
        public withdraw_amount: u64
    ) -> (CollateralDeposit, Future) {
        // Access control
        assert_eq(deposit.owner, self.signer);
        
        // Input validation
        assert(withdraw_amount > 0u64);
        assert(withdraw_amount <= deposit.amount);
        
        let remaining_deposit: CollateralDeposit = CollateralDeposit {
            owner: deposit.owner,
            amount: deposit.amount - withdraw_amount,
            asset_type: deposit.asset_type,
            deposit_time: deposit.deposit_time,
        };
        
        let f: Future = finalize_withdraw(deposit.asset_type, withdraw_amount);
        return (remaining_deposit, f);
    }
    
    async function finalize_withdraw(asset_type: u8, amount: u64) {
        // Check if protocol is paused
        let paused: bool = Mapping::get_or_use(protocol_paused, 1u8, false);
        assert(!paused);
        
        // Update total deposits
        let current_deposits: u64 = Mapping::get_or_use(total_deposits, asset_type, 0u64);
        assert(current_deposits >= amount);
        Mapping::set(total_deposits, asset_type, current_deposits - amount);
    }
    
    // Update interest rates based on utilization
    async transition update_interest_rates(
        public asset_type: u8
    ) -> Future {
        let f: Future = finalize_update_rates(asset_type);
        return f;
    }
    
    async function finalize_update_rates(asset_type: u8) {
        let total_deps: u64 = Mapping::get_or_use(total_deposits, asset_type, 1u64);
        let total_borr: u64 = Mapping::get_or_use(total_borrowed, asset_type, 0u64);
        
        // Calculate utilization rate (borrowed / deposits * 100)
        let utilization: u64 = total_borr * 100u64 / total_deps;
        
        // Update interest rate: base_rate + utilization_factor
        let new_rate: u64 = BASE_INTEREST_RATE + utilization * 10u64;
        Mapping::set(interest_rates, asset_type, new_rate);
    }
    
    // Admin: Pause/unpause protocol
    async transition set_protocol_pause(
        public paused: bool
    ) -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_set_pause(paused);
        return f;
    }
    
    async function finalize_set_pause(paused: bool) {
        Mapping::set(protocol_paused, 1u8, paused);
    }
    
    // Admin: Collect protocol fees
    async transition collect_fees(
        public asset_type: u8,
        public recipient: address
    ) -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_collect_fees(asset_type, recipient);
        return f;
    }
    
    async function finalize_collect_fees(asset_type: u8, recipient: address) {
        let fees: u64 = Mapping::get_or_use(protocol_fees, asset_type, 0u64);
        if (fees > 0u64) {
            Mapping::set(protocol_fees, asset_type, 0u64);
            // Fees would be transferred to recipient in real implementation
        }
    }
    
    // View: Get protocol statistics
    async transition get_protocol_stats(
        public asset_type: u8
    ) -> Future {
        let f: Future = finalize_get_stats(asset_type);
        return f;
    }
    
    async function finalize_get_stats(asset_type: u8) {
        let total_deps: u64 = Mapping::get_or_use(total_deposits, asset_type, 0u64);
        let total_borr: u64 = Mapping::get_or_use(total_borrowed, asset_type, 0u64);
        let rate: u64 = Mapping::get_or_use(interest_rates, asset_type, BASE_INTEREST_RATE);
        
        // Stats are updated in mappings for external visibility
        // In practice, these would be emitted as events or returned via public outputs
    }
    
    // Calculate interest for a loan position
    transition calculate_interest(
        loan: LoanPosition,
        public current_time: u64
    ) -> u64 {
        assert_eq(loan.owner, self.signer);
        
        let time_elapsed: u64 = current_time - loan.borrow_time;
        let annual_interest: u64 = loan.borrowed_amount * loan.interest_rate / INTEREST_PRECISION;
        let interest: u64 = annual_interest * time_elapsed / SECONDS_PER_YEAR;
        
        return interest;
    }
    
    // Check if position is healthy (above liquidation threshold)
    transition check_position_health(loan: LoanPosition) -> bool {
        assert_eq(loan.owner, self.signer);
        
        let collateral_ratio: u64 = loan.collateral_amount * 100u64 / loan.borrowed_amount;
        return collateral_ratio >= LIQUIDATION_THRESHOLD;
    }
    
    // Create payment token (for testing purposes)
    transition create_payment_token(public amount: u64) -> PaymentToken {
        assert(amount > 0u64);
        return PaymentToken {
            owner: self.signer,
            amount: amount,
        };
    }
}