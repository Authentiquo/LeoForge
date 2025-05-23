program orderbook_dex.aleo {
    // Token record representing different tokens by ID
    record Token {
        owner: address,
        token_id: field,
        amount: u128,
    }
    
    // Receipt record for order creators
    record Receipt {
        owner: address,
        order_id: field,
    }
    
    // Order struct stored in mapping
    struct Order {
        creator: address,
        sold_token_id: field,
        bought_token_id: field,
        sold_token_amount: u128,
        bought_token_amount: u128,
        accepted: bool,
        withdrawn: bool,
    }
    
    // Mapping to store orders
    mapping orders: field => Order;
    
    // Mapping to store program's token balances (token_id => amount)
    mapping token_balances: field => u128;
    
    // Create a new order
    // User provides their sold token (private) and specifies what they want to buy
    async transition create_order(
        order_id: field,
        sold_token: Token,
        bought_token_id: field,
        bought_token_amount: u128,
    ) -> (Receipt, Future) {
        // Ensure the caller owns the sold token
        assert_eq(sold_token.owner, self.caller);
        
        // Create receipt for the order creator
        let receipt: Receipt = Receipt {
            owner: self.caller,
            order_id: order_id,
        };
        
        // Store the order and transfer sold tokens to program
        return (receipt, store_new_order(
            order_id,
            self.caller,
            sold_token.token_id,
            bought_token_id,
            sold_token.amount,
            bought_token_amount
        ));
    }
    
    // Async function to store order and update program's token balance
    async function store_new_order(
        order_id: field,
        creator: address,
        sold_token_id: field,
        bought_token_id: field,
        sold_token_amount: u128,
        bought_token_amount: u128,
    ) {
        // Ensure order doesn't exist yet
        let order_exists: bool = Mapping::contains(orders, order_id);
        assert(!order_exists);
        
        // Create new order struct
        let new_order: Order = Order {
            creator: creator,
            sold_token_id: sold_token_id,
            bought_token_id: bought_token_id,
            sold_token_amount: sold_token_amount,
            bought_token_amount: bought_token_amount,
            accepted: false,
            withdrawn: false,
        };
        
        // Store the order in mapping
        Mapping::set(orders, order_id, new_order);
        
        // Add sold tokens to program's balance (private to public transfer)
        let current_balance: u128 = Mapping::get_or_use(token_balances, sold_token_id, 0u128);
        Mapping::set(token_balances, sold_token_id, current_balance + sold_token_amount);
    }
    
    // Accept an existing order
    // User provides bought tokens and receives sold tokens
    async transition accept_order(
        order_id: field,
        bought_token: Token,
    ) -> (Token, Future) {
        // Ensure the caller owns the bought token
        assert_eq(bought_token.owner, self.caller);
        
        // We need to get order info to create the sold token for accepter
        // Since we can't access mappings in transitions, we'll create a placeholder
        // The async function will validate everything
        let sold_token_for_accepter: Token = Token {
            owner: self.caller,
            token_id: 1field, // Placeholder - will be validated in async function
            amount: 1u128,    // Placeholder - will be validated in async function
        };
        
        return (sold_token_for_accepter, process_order_acceptance(
            order_id,
            bought_token.token_id,
            bought_token.amount,
            self.caller
        ));
    }
    
    // Async function to process order acceptance
    async function process_order_acceptance(
        order_id: field,
        bought_token_id: field,
        bought_token_amount: u128,
        accepter: address,
    ) {
        // Get the order
        let order: Order = Mapping::get(orders, order_id);
        
        // Verify order exists and hasn't been accepted yet
        assert(!order.accepted);
        assert(!order.withdrawn);
        
        // Verify accepter is not the creator
        assert_neq(order.creator, accepter);
        
        // Verify token types and amounts match
        assert_eq(order.bought_token_id, bought_token_id);
        assert_eq(order.bought_token_amount, bought_token_amount);
        
        // Update order as accepted
        let updated_order: Order = Order {
            creator: order.creator,
            sold_token_id: order.sold_token_id,
            bought_token_id: order.bought_token_id,
            sold_token_amount: order.sold_token_amount,
            bought_token_amount: order.bought_token_amount,
            accepted: true,
            withdrawn: order.withdrawn,
        };
        
        Mapping::set(orders, order_id, updated_order);
        
        // Update token balances
        // Add bought tokens to program balance (private to public)
        let bought_balance: u128 = Mapping::get_or_use(token_balances, bought_token_id, 0u128);
        Mapping::set(token_balances, bought_token_id, bought_balance + bought_token_amount);
        
        // Remove sold tokens from program balance (public to private transfer to accepter)
        let sold_balance: u128 = Mapping::get(token_balances, order.sold_token_id);
        assert(sold_balance >= order.sold_token_amount);
        Mapping::set(token_balances, order.sold_token_id, sold_balance - order.sold_token_amount);
    }
    
    // Delete an unaccepted order
    // Order creator can cancel their order and get their sold tokens back
    async transition delete_order(
        receipt: Receipt,
    ) -> (Token, Future) {
        // Ensure caller owns the receipt
        assert_eq(receipt.owner, self.caller);
        
        // Create placeholder token that will be returned to creator
        let returned_token: Token = Token {
            owner: self.caller,
            token_id: 1field, // Placeholder - will be set based on order
            amount: 1u128,    // Placeholder - will be set based on order
        };
        
        return (returned_token, process_order_deletion(receipt.order_id, self.caller));
    }
    
    // Async function to process order deletion
    async function process_order_deletion(
        order_id: field,
        caller: address,
    ) {
        // Get the order
        let order: Order = Mapping::get(orders, order_id);
        
        // Verify caller is the order creator
        assert_eq(order.creator, caller);
        
        // Verify order hasn't been accepted yet
        assert(!order.accepted);
        assert(!order.withdrawn);
        
        // Remove the order from mapping
        Mapping::remove(orders, order_id);
        
        // Return sold tokens to creator (public to private transfer)
        let sold_balance: u128 = Mapping::get(token_balances, order.sold_token_id);
        assert(sold_balance >= order.sold_token_amount);
        Mapping::set(token_balances, order.sold_token_id, sold_balance - order.sold_token_amount);
    }
    
    // Withdraw bought tokens after order acceptance
    // Order creator uses receipt to claim their bought tokens
    async transition withdraw(
        receipt: Receipt,
    ) -> (Token, Future) {
        // Ensure caller owns the receipt
        assert_eq(receipt.owner, self.caller);
        
        // Create placeholder token for bought tokens
        let bought_token: Token = Token {
            owner: self.caller,
            token_id: 1field, // Placeholder - will be set based on order
            amount: 1u128,    // Placeholder - will be set based on order
        };
        
        return (bought_token, process_withdrawal(receipt.order_id, self.caller));
    }
    
    // Async function to process withdrawal
    async function process_withdrawal(
        order_id: field,
        caller: address,
    ) {
        // Get the order
        let order: Order = Mapping::get(orders, order_id);
        
        // Verify caller is the order creator
        assert_eq(order.creator, caller);
        
        // Verify order has been accepted but not withdrawn yet
        assert(order.accepted);
        assert(!order.withdrawn);
        
        // Update order as withdrawn
        let updated_order: Order = Order {
            creator: order.creator,
            sold_token_id: order.sold_token_id,
            bought_token_id: order.bought_token_id,
            sold_token_amount: order.sold_token_amount,
            bought_token_amount: order.bought_token_amount,
            accepted: order.accepted,
            withdrawn: true,
        };
        
        Mapping::set(orders, order_id, updated_order);
        
        // Transfer bought tokens to creator (public to private transfer)
        let bought_balance: u128 = Mapping::get(token_balances, order.bought_token_id);
        assert(bought_balance >= order.bought_token_amount);
        Mapping::set(token_balances, order.bought_token_id, bought_balance - order.bought_token_amount);
    }
}