program simple_token.aleo {
    // Admin address for minting authorization
    const ADMIN: address = aleo1qgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqanmpl0;
    
    // Token record for private balances
    record Token {
        owner: address,
        amount: u64,
    }
    
    // Public mapping for total supply tracking
    mapping total_supply: u8 => u64;
    
    // Private token transfer between addresses
    transition transfer(token: Token, to: address, amount: u64) -> (Token, Token) {
        // Verify the caller owns the token
        assert_eq(token.owner, self.signer);
        
        // Ensure transfer amount is valid
        assert(amount > 0u64);
        assert(amount <= token.amount);
        
        // Create tokens for recipient and change for sender
        let recipient_token: Token = Token {
            owner: to,
            amount: amount,
        };
        
        let change_token: Token = Token {
            owner: self.signer,
            amount: token.amount - amount,
        };
        
        return (recipient_token, change_token);
    }
    
    // Public mint function with supply tracking
    async transition mint(public to: address, public amount: u64) -> (Token, Future) {
        // Only admin can mint new tokens
        assert_eq(self.signer, ADMIN);
        
        // Ensure mint amount is positive
        assert(amount > 0u64);
        
        // Create new token for recipient
        let new_token: Token = Token {
            owner: to,
            amount: amount,
        };
        
        // Update total supply in mapping
        let f: Future = finalize_mint(amount);
        
        return (new_token, f);
    }
    
    // Finalize mint by updating total supply
    async function finalize_mint(amount: u64) {
        // Get current supply or default to 0
        let current_supply: u64 = Mapping::get_or_use(total_supply, 1u8, 0u64);
        
        // Check for overflow
        assert(current_supply + amount >= current_supply);
        
        // Update total supply
        Mapping::set(total_supply, 1u8, current_supply + amount);
    }
    
    // Burn tokens and update supply
    async transition burn(token: Token, amount: u64) -> (Token, Future) {
        // Verify the caller owns the token
        assert_eq(token.owner, self.signer);
        
        // Ensure burn amount is valid
        assert(amount > 0u64);
        assert(amount <= token.amount);
        
        // Create remaining token after burn
        let remaining_token: Token = Token {
            owner: self.signer,
            amount: token.amount - amount,
        };
        
        // Update total supply in mapping
        let f: Future = finalize_burn(amount);
        
        return (remaining_token, f);
    }
    
    // Finalize burn by decreasing total supply
    async function finalize_burn(amount: u64) {
        // Get current supply
        let current_supply: u64 = Mapping::get_or_use(total_supply, 1u8, 0u64);
        
        // Ensure sufficient supply to burn
        assert(current_supply >= amount);
        
        // Update total supply
        Mapping::set(total_supply, 1u8, current_supply - amount);
    }
    
    // Public function to view total supply
    async transition get_supply() -> Future {
        let f: Future = finalize_get_supply();
        return f;
    }
    
    async function finalize_get_supply() {
        // This allows public visibility of total supply
        let supply: u64 = Mapping::get_or_use(total_supply, 1u8, 0u64);
    }
}