import token_registry.aleo;
import credits.aleo;

program my_arc21_token.aleo {
    // Token metadata constants
    const TOKEN_ID: field = 1234567890123456789field;
    const MAX_SUPPLY: u128 = 1000000000000u128; // 1 million tokens (with 6 decimals)
    const TOKEN_NAME: u128 = 77121065114099050050049084111107101110u128; // "MyArc21Token" as u128
    const TOKEN_SYMBOL: u128 = 77065084u128; // "MAT" as u128
    const DECIMALS: u8 = 6u8;
    
    // Mint parameters
    const MINT_START_HEIGHT: u32 = 1000u32; // Minting allowed after block 1000
    const MINT_PRICE: u64 = 1000000u64; // 1 credit per token (in microcredits)
    const TREASURY: address = aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc;
    
    // Authorization settings
    const EXTERNAL_AUTH_REQUIRED: bool = false;
    const EXTERNAL_AUTH_PARTY: address = aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc;
    const AUTHORIZED_UNTIL: u32 = 4294967295u32; // Max u32 value (never expires)
    
    // Mapping to track if token has been initialized
    mapping is_initialized: bool => bool;
    
    // Initialize the token by registering it with the token registry
    async transition initialize() -> Future {
        return finalize_initialize();
    }
    
    async function finalize_initialize() {
        // Check if already initialized
        let already_initialized: bool = Mapping::get_or_use(is_initialized, true, false);
        assert_eq(already_initialized, false);
        
        // Mark as initialized
        Mapping::set(is_initialized, true, true);
    }
    
    // Separate transition to register with token registry (must be called after initialize)
    async transition register_with_registry() -> Future {
        let register_future: Future = token_registry.aleo/register_token(
            TOKEN_ID,
            TOKEN_NAME,
            TOKEN_SYMBOL,
            DECIMALS,
            MAX_SUPPLY,
            EXTERNAL_AUTH_REQUIRED,
            EXTERNAL_AUTH_PARTY
        );
        return finalize_register_with_registry(register_future);
    }
    
    async function finalize_register_with_registry(register_future: Future) {
        // Ensure token is initialized locally before registering
        let initialized: bool = Mapping::get(is_initialized, true);
        assert(initialized);
        
        // Await the registration completion
        register_future.await();
    }
    
    // Mint tokens - requires payment to treasury and minimum block height
    async transition mint(
        public amount: u128,
        public current_height: u32,
        private credits_record: credits.aleo/credits
    ) -> (credits.aleo/credits, credits.aleo/credits, Future) {
        // Check if minting is allowed (block height requirement)
        assert(current_height >= MINT_START_HEIGHT);
        
        // Calculate total payment required
        let total_payment: u64 = (amount as u64) * MINT_PRICE;
        
        // Ensure the credits record has enough balance
        assert(credits_record.microcredits >= total_payment);
        
        // Transfer payment to treasury
        let (remaining_credits, treasury_credits): (credits.aleo/credits, credits.aleo/credits) = 
            credits.aleo/transfer_private(
                credits_record,
                TREASURY,
                total_payment
            );
        
        // Call token registry to mint tokens
        let mint_future: Future = token_registry.aleo/mint_public(
            TOKEN_ID,
            self.caller,
            amount,
            AUTHORIZED_UNTIL
        );
        
        return (remaining_credits, treasury_credits, finalize_mint(mint_future, current_height));
    }
    
    // Finalize the minting process
    async function finalize_mint(mint_future: Future, current_height: u32) {
        // Ensure token is initialized
        let initialized: bool = Mapping::get(is_initialized, true);
        assert(initialized);
        
        // Ensure block height requirement is met
        assert(current_height >= MINT_START_HEIGHT);
        
        // Await the minting completion from token registry
        mint_future.await();
    }
    
    // Update the token admin - only current admin can call this
    async transition update_admin(public new_admin: address) -> Future {
        let update_future: Future = token_registry.aleo/update_token_management(
            TOKEN_ID,
            new_admin,
            EXTERNAL_AUTH_PARTY
        );
        return finalize_update_admin(update_future);
    }
    
    async function finalize_update_admin(update_future: Future) {
        // Ensure token is initialized
        let initialized: bool = Mapping::get(is_initialized, true);
        assert(initialized);
        
        // Await the admin update completion
        update_future.await();
    }
    
    // Helper function to get token info
    transition get_token_info() -> (field, u128, u128, u8, u128) {
        return (TOKEN_ID, TOKEN_NAME, TOKEN_SYMBOL, DECIMALS, MAX_SUPPLY);
    }
    
    // Check if token is initialized
    async transition check_initialization() -> Future {
        return finalize_check_initialization();
    }
    
    async function finalize_check_initialization() {
        let initialized: bool = Mapping::get_or_use(is_initialized, true, false);
        // Note: This will succeed if initialized, fail if not
        assert(initialized);
    }
}

// Commands to deploy and initialize the token:
// 1. First deploy: leo deploy
// 2. Initialize: leo execute initialize
// 3. Register with token registry: leo execute register_with_registry