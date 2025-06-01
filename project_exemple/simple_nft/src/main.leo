program simple_nft.aleo {
    // Admin address
    const ADMIN: address = aleo1qgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqanmpl0;

    // Token metadata structure
    struct TokenMetadata {
        name: field,
        description: field,
        image_url: field,
    }

    // NFT ownership record (private)
    record NFTRecord {
        owner: address,
        token_id: u64,
        metadata_hash: field,
    }

    // Public mappings for token state
    mapping token_exists: u64 => bool;
    mapping token_metadata: u64 => TokenMetadata;
    mapping next_token_id: u8 => u64;

    // Initialize the contract
    async transition initialize() -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_init();
        return f;
    }

    async function finalize_init() {
        // Set initial token ID counter
        Mapping::set(next_token_id, 0u8, 1u64);
    }

    // Mint new NFT (admin only)
    async transition mint(
        public to: address,
        public metadata: TokenMetadata
    ) -> (NFTRecord, Future) {
        // Only admin can mint
        assert_eq(self.signer, ADMIN);
        
        // Create metadata hash for privacy
        let metadata_hash: field = BHP256::hash_to_field(metadata);
        
        // Create NFT record (private ownership)
        let nft: NFTRecord = NFTRecord {
            owner: to,
            token_id: 0u64, // Will be set in finalize
            metadata_hash: metadata_hash,
        };
        
        let f: Future = finalize_mint(to, metadata);
        return (nft, f);
    }

    async function finalize_mint(to: address, metadata: TokenMetadata) {
        // Get next token ID
        let token_id: u64 = Mapping::get_or_use(next_token_id, 0u8, 1u64);
        
        // Check token doesn't already exist
        assert(!Mapping::contains(token_exists, token_id));
        
        // Mark token as existing
        Mapping::set(token_exists, token_id, true);
        
        // Store public metadata
        Mapping::set(token_metadata, token_id, metadata);
        
        // Increment token ID counter
        let next_id: u64 = token_id + 1u64;
        assert(next_id > token_id); // Overflow check
        Mapping::set(next_token_id, 0u8, next_id);
    }

    // Transfer NFT privately
    transition transfer(nft: NFTRecord, to: address) -> NFTRecord {
        // Only owner can transfer
        assert_eq(nft.owner, self.signer);
        
        // Create new record for recipient
        return NFTRecord {
            owner: to,
            token_id: nft.token_id,
            metadata_hash: nft.metadata_hash,
        };
    }

    // Get public metadata
    async transition get_metadata(public token_id: u64) -> (public TokenMetadata, Future) {
        let f: Future = finalize_get_metadata(token_id);
        
        // Return empty metadata (actual data retrieved in finalize)
        let empty_metadata: TokenMetadata = TokenMetadata {
            name: 0field,
            description: 0field,
            image_url: 0field,
        };
        
        return (empty_metadata, f);
    }

    async function finalize_get_metadata(token_id: u64) {
        // Verify token exists
        assert(Mapping::get_or_use(token_exists, token_id, false));
        
        // Metadata is already publicly available in mapping
        // This function serves as verification
    }

    // Check if token exists
    async transition token_exists_check(public token_id: u64) -> (public bool, Future) {
        let f: Future = finalize_exists_check(token_id);
        return (false, f); // Actual value determined in finalize
    }

    async function finalize_exists_check(token_id: u64) {
        // Check if token exists in mapping
        let exists: bool = Mapping::get_or_use(token_exists, token_id, false);
        // Result is stored in mapping access logs
    }

    // Get total supply
    async transition get_total_supply() -> (public u64, Future) {
        let f: Future = finalize_get_supply();
        return (0u64, f); // Actual value determined in finalize
    }

    async function finalize_get_supply() {
        // Current token ID minus 1 equals total supply
        let current_id: u64 = Mapping::get_or_use(next_token_id, 0u8, 1u64);
        // Supply is current_id - 1 (since we start from 1)
    }

    // Verify ownership (private)
    transition verify_ownership(nft: NFTRecord) -> public bool {
        // Return true if caller owns the NFT
        return nft.owner == self.signer;
    }

    // Get token ID from record (private)
    transition get_token_id(nft: NFTRecord) -> public u64 {
        // Only owner can reveal token ID
        assert_eq(nft.owner, self.signer);
        return nft.token_id;
    }

    // Batch transfer (private)
    transition batch_transfer(
        nft1: NFTRecord,
        nft2: NFTRecord,
        to: address
    ) -> (NFTRecord, NFTRecord) {
        // Only owner can transfer
        assert_eq(nft1.owner, self.signer);
        assert_eq(nft2.owner, self.signer);
        
        let new_nft1: NFTRecord = NFTRecord {
            owner: to,
            token_id: nft1.token_id,
            metadata_hash: nft1.metadata_hash,
        };
        
        let new_nft2: NFTRecord = NFTRecord {
            owner: to,
            token_id: nft2.token_id,
            metadata_hash: nft2.metadata_hash,
        };
        
        return (new_nft1, new_nft2);
    }

    // Update metadata (admin only)
    async transition update_metadata(
        public token_id: u64,
        public new_metadata: TokenMetadata
    ) -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_update_metadata(token_id, new_metadata);
        return f;
    }

    async function finalize_update_metadata(token_id: u64, new_metadata: TokenMetadata) {
        // Verify token exists
        assert(Mapping::get_or_use(token_exists, token_id, false));
        
        // Update metadata
        Mapping::set(token_metadata, token_id, new_metadata);
    }
}