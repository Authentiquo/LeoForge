program simple_voting.aleo {
    // Admin address for controlling the voting system
    const ADMIN: address = aleo1qgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqanmpl0;
    
    // Vote token record for private voting
    record VoteToken {
        owner: address,
        proposal_id: field,
        token_id: field,
    }
    
    // Mappings for public state
    mapping registered_voters: address => bool;
    mapping vote_tallies: field => u64;
    mapping vote_nullifiers: field => bool;
    mapping voting_active: field => bool;
    mapping total_votes_cast: field => u64;
    
    // Register a voter (admin only)
    async transition register_voter(public voter: address, public proposal_id: field) -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_register(voter, proposal_id);
        return f;
    }
    
    async function finalize_register(voter: address, proposal_id: field) {
        // Check if voting is still active for this proposal
        let active: bool = Mapping::get_or_use(voting_active, proposal_id, true);
        assert(active);
        
        // Register the voter
        Mapping::set(registered_voters, voter, true);
    }
    
    // Issue vote token to registered voter (admin only)
    async transition issue_vote_token(public voter: address, public proposal_id: field) -> (VoteToken, Future) {
        assert_eq(self.signer, ADMIN);
        
        let f: Future = finalize_issue_token(voter, proposal_id);
        return (VoteToken { owner: voter, proposal_id: proposal_id, token_id: 0field }, f);
    }
    
    async function finalize_issue_token(voter: address, proposal_id: field) {
        // Verify voter is registered
        let is_registered: bool = Mapping::get_or_use(registered_voters, voter, false);
        assert(is_registered);
        
        // Check if voting is still active
        let active: bool = Mapping::get_or_use(voting_active, proposal_id, true);
        assert(active);
        
        // Create unique token ID using voter address, proposal and block height
        let token_id: field = BHP256::hash_to_field(voter) + BHP256::hash_to_field(proposal_id) + (block.height as field);
        
        // Ensure token hasn't been issued before (prevent double voting)
        let nullifier_exists: bool = Mapping::get_or_use(vote_nullifiers, token_id, false);
        assert(!nullifier_exists);
        
        // Mark this token as issued
        Mapping::set(vote_nullifiers, token_id, true);
    }
    
    // Cast vote privately (consumes vote token)
    async transition cast_vote(vote_token: VoteToken, public vote_choice: bool) -> Future {
        // Verify token ownership
        assert_eq(vote_token.owner, self.signer);
        
        let f: Future = finalize_cast_vote(vote_token.proposal_id, vote_choice, vote_token.token_id, self.signer);
        return f;
    }
    
    async function finalize_cast_vote(proposal_id: field, vote_choice: bool, token_id: field, signer: address) {
        // Check if voting is still active
        let active: bool = Mapping::get_or_use(voting_active, proposal_id, true);
        assert(active);
        
        // Verify token was properly issued
        let token_issued: bool = Mapping::get_or_use(vote_nullifiers, token_id, false);
        assert(token_issued);
        
        // Create nullifier to prevent double voting
        let nullifier: field = BHP256::hash_to_field(token_id) + BHP256::hash_to_field(signer) + (vote_choice ? 1field : 0field);
        
        // Check if this specific vote has already been cast
        let vote_cast: bool = Mapping::get_or_use(vote_nullifiers, nullifier, false);
        assert(!vote_cast);
        
        // Mark this vote as cast
        Mapping::set(vote_nullifiers, nullifier, true);
        
        // Update vote tally based on vote choice
        if (vote_choice) {
            // Vote YES - increment yes votes
            let yes_key: field = BHP256::hash_to_field(proposal_id) + 1field;
            let yes_votes: u64 = Mapping::get_or_use(vote_tallies, yes_key, 0u64);
            assert(yes_votes + 1u64 >= yes_votes); // Overflow check
            Mapping::set(vote_tallies, yes_key, yes_votes + 1u64);
        } else {
            // Vote NO - increment no votes
            let no_key: field = BHP256::hash_to_field(proposal_id) + 0field;
            let no_votes: u64 = Mapping::get_or_use(vote_tallies, no_key, 0u64);
            assert(no_votes + 1u64 >= no_votes); // Overflow check
            Mapping::set(vote_tallies, no_key, no_votes + 1u64);
        }
        
        // Update total votes cast for this proposal
        let total: u64 = Mapping::get_or_use(total_votes_cast, proposal_id, 0u64);
        assert(total + 1u64 >= total); // Overflow check
        Mapping::set(total_votes_cast, proposal_id, total + 1u64);
    }
    
    // Get vote results (public view)
    async transition get_results(public proposal_id: field) -> Future {
        let f: Future = finalize_get_results(proposal_id);
        return f;
    }
    
    async function finalize_get_results(proposal_id: field) {
        // This function exists to make results publicly readable
        // The actual tallies are stored in the mappings and can be queried
        let yes_key: field = BHP256::hash_to_field(proposal_id) + 1field;
        let no_key: field = BHP256::hash_to_field(proposal_id) + 0field;
        
        let yes_votes: u64 = Mapping::get_or_use(vote_tallies, yes_key, 0u64);
        let no_votes: u64 = Mapping::get_or_use(vote_tallies, no_key, 0u64);
        let total: u64 = Mapping::get_or_use(total_votes_cast, proposal_id, 0u64);
        
        // Results are accessible through mapping queries
        // Total votes should equal yes + no votes
        assert_eq(total, yes_votes + no_votes);
    }
    
    // Close voting (admin only)
    async transition close_voting(public proposal_id: field) -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_close_voting(proposal_id);
        return f;
    }
    
    async function finalize_close_voting(proposal_id: field) {
        // Mark voting as inactive
        Mapping::set(voting_active, proposal_id, false);
    }
    
    // Open voting (admin only) 
    async transition open_voting(public proposal_id: field) -> Future {
        assert_eq(self.signer, ADMIN);
        let f: Future = finalize_open_voting(proposal_id);
        return f;
    }
    
    async function finalize_open_voting(proposal_id: field) {
        // Mark voting as active
        Mapping::set(voting_active, proposal_id, true);
    }
    
    // Check if voter is registered (public view)
    async transition check_voter_status(public voter: address) -> Future {
        let f: Future = finalize_check_voter(voter);
        return f;
    }
    
    async function finalize_check_voter(voter: address) {
        // This makes voter registration status publicly queryable
        let is_registered: bool = Mapping::get_or_use(registered_voters, voter, false);
        // Status can be queried from mapping
    }
}