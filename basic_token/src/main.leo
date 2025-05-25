// A basic fungible token implementation for Aleo
program basic_token.aleo {
    // Record definition for the token
    record Token {
        // The token owner
        owner: address,
        // The token amount
        amount: u64,
    }

    // Mapping to track public minting authorization
    mapping authorized_minters: address => bool;

    // Initialize program owner as authorized minter
    async transition initialize_minter(minter: address) -> Future {
        let fut: Future = finalize_initialize_minter(minter);
        return fut;
    }

    async function finalize_initialize_minter(minter: address) {
        Mapping::set(authorized_minters, minter, true);
    }

    // Mint new tokens to a specified receiver
    async transition mint(receiver: address, amount: u64) -> Future {
        // Ensure amount is non-zero
        assert(amount > 0u64);

        let fut: Future = finalize_mint(self.caller);
        return fut;
    }

    async function finalize_mint(caller: address) {
        // Verify caller is authorized to mint
        let is_authorized: bool = Mapping::get_or_use(authorized_minters, caller, false);
        assert(is_authorized);
    }

    // Helper transition to create token record after minting authorization
    transition mint_token(receiver: address, amount: u64) -> Token {
        // Create new token record
        let token: Token = Token {
            owner: receiver,
            amount: amount,
        };
        return token;
    }

    // Transfer tokens between addresses
    transition transfer(
        token: Token,
        receiver: address,
        amount: u64
    ) -> (Token, Token) {
        // Validate transfer amount
        assert(amount > 0u64);
        assert(amount <= token.amount);

        // Validate ownership
        assert_eq(token.owner, self.caller);

        // Create token record for receiver
        let recipient_token: Token = Token {
            owner: receiver,
            amount: amount,
        };

        // Create remaining token record for sender
        let sender_token: Token = Token {
            owner: self.caller,
            amount: token.amount - amount,
        };

        // Return both token records
        return (recipient_token, sender_token);
    }
}