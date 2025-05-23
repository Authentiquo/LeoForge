# Leo Programming Language Cheatsheet

## Program Structure

```leo
// Program declaration
program my_program.aleo {
    // Program code goes here
}
```

## Data Types

- `u8`, `u16`, `u32`, `u64`, `u128`: Unsigned integers
- `i8`, `i16`, `i32`, `i64`, `i128`: Signed integers
- `field`: Field element (for cryptographic operations)
- `group`: Group element (for elliptic curve operations)
- `address`: Aleo account address
- `bool`: Boolean (true/false)
- `scalar`: Scalar value for cryptographic operations

## Records

```leo
// Define a record
record token {
    // Public field (visible on the blockchain)
    owner: address.public,
    // Private field (encrypted on the blockchain)
    amount: u64.private,
}
```

## Functions (Transitions)

```leo
// Public function (anyone can call)
transition mint(amount: u64) -> token {
    return token {
        owner: self.caller,
        amount: amount,
    };
}

// Function with multiple outputs
transition transfer(receiver: address, amount: u64, input: token) -> (token, token) {
    let remaining: u64 = input.amount - amount;
    
    let sender_token: token = token {
        owner: self.caller,
        amount: remaining,
    };
    
    let receiver_token: token = token {
        owner: receiver,
        amount: amount,
    };
    
    return (sender_token, receiver_token);
}
```

## Asynchronous Programming Model

### Async Transitions

Async transitions are used for executing on-chain computations. They can produce a `Future` object and update on-chain state through mappings.

```leo
// Async transition to mint tokens and update a public balance
async transition mint_public(
    public receiver: address,
    public amount: u64,
) -> (token, Future) {
    // Create a token
    let new_token: token = token {
        owner: receiver,
        amount,
    };
    
    // Call async function and return its Future
    return (new_token, update_balance(receiver, amount));
}
```

### Async Functions

Async functions are used to manage on-chain state. They must be called from async transitions and return a `Future`.

```leo
// Async function to update a user's balance in a mapping
async function update_balance(
    public user: address,
    public amount: u64,
) {
    // Get current balance or use 0 if not found
    let current_balance: u64 = Mapping::get_or_use(balances, user, 0u64);
    
    // Update the mapping
    Mapping::set(balances, user, current_balance + amount);
}
```

### Futures

Futures represent computation that will execute on-chain. They're produced by async functions and can be composed.

```leo
// Return a Future from an async transition
async transition process_transaction(
    public sender: address,
    public receiver: address,
    public amount: u64,
) -> Future {
    // If this returns a Future
    return update_balances(sender, receiver, amount);
}

// Await multiple Futures in an async function
async function update_balances(
    public sender: address,
    public receiver: address,
    public amount: u64,
) {
    // Get current balances
    let sender_balance: u64 = Mapping::get(balances, sender);
    let receiver_balance: u64 = Mapping::get_or_use(balances, receiver, 0u64);
    
    // Update balances
    Mapping::set(balances, sender, sender_balance - amount);
    Mapping::set(balances, receiver, receiver_balance + amount);
}
```

### Rules of Async Programming in Leo

1. Async functions can only be called from async transitions
2. Async functions cannot return values (only a Future)
3. Async transitions cannot be called inside conditional blocks
4. All Futures must be consumed by an async function call or returned as output

## Mappings (On-chain Storage)

```leo
// Define a mapping
mapping balances: address => u64;
```

### Mapping Operations

```leo
// In an async function:

// Get a value from a mapping
let value: u64 = Mapping::get(balances, user);

// Get a value or use default if not found
let value: u64 = Mapping::get_or_use(balances, user, 0u64);

// Check if a key exists in a mapping
let exists: bool = Mapping::contains(balances, user);

// Set a value in a mapping
Mapping::set(balances, user, 100u64);

// Remove a key-value pair from a mapping
Mapping::remove(balances, user);
```

## Special Variables

```leo
// Get the caller's address
let caller: address = self.caller;

// Get the signer's address (originator of transaction)
let signer: address = self.signer;
```

## Importing Other Programs

```leo
// Import another program
import token.aleo;

program my_program.aleo {
    // Use imported program
    transition use_token(token_record: token.aleo/token) {
        // ...
    }
}
```

## Control Flow

```leo
// Conditionals
transition conditional_example(a: u32, b: u32) -> u32 {
    let result: u32 = 0u32;
    
    if a > b {
        result = a - b;
    } else {
        result = b - a;
    }
    
    return result;
}
```

## Complete Example: Reward Points System

```leo
program reward_system.aleo {
    // Mapping to store user balances on-chain  
    mapping user_balances: address => u64;
  
    // Transition function to add reward points for a user  
    async transition add_points(  
        public user: address,  
        public points: u64,  
        public is_special: bool,  
    ) -> Future {  
        // Update the user's points asynchronously  
        return update_user_balance(user, points, is_special);  
    }  
  
    // Async function to update the user's balance  
    async function update_user_balance(  
        user: address,  
        points: u64,  
        is_special: bool,  
    ) {  
        // Retrieve the current balance or initialize to 0  
        let current_balance: u64 = Mapping::get_or_use(user_balances, user, 0u64);  
  
        // Calculate bonus points
        let bonus_points = calculate_bonus(points);  
        let total_points = double_points_if_special(points + bonus_points, is_special);  
  
        // Update the mapping with the new balance  
        Mapping::set(user_balances, user, current_balance + total_points);  
    }  
  
    // Helper function to calculate a 10% bonus on points  
    function calculate_bonus(points: u64) -> u64 {  
        let bonus_rate: u32 = 10; // 10% bonus  
        return (points * bonus_rate as u64) / 100;  
    }  
  
    // Inline function to double the points if a special condition is met  
    inline double_points_if_special(points: u64, is_special: bool) -> u64 {  
        return if is_special { points * 2 } else { points };  
    }  
}
```

## Best Practices

1. **Design for Atomicity**: Ensure async functions handle failures gracefully
2. **Minimize Mapping Operations**: Avoid unnecessary reads/writes to reduce costs
3. **Combine Related Operations**: Group related mapping operations in the same async function
4. **Use Helper Functions**: Break down complex logic into reusable functions

## Common Mistakes to Avoid

1. Using Rust syntax instead of Leo syntax
2. Forgetting visibility modifiers (`.public` or `.private`)
3. Not initializing values properly
4. Using incorrect types or type conversions
5. Incorrect record field access
6. Not handling ownership properly in transitions
7. Calling async functions from non-async transitions
8. Returning values from async functions (instead of Futures)
9. Not awaiting or returning all Futures
10. Trying to use mapping operations outside of async functions

## Debugging Tips

1. Check state before/after mapping operations using temporary log outputs
2. Verify visibility modifiers match expected usage
3. Ensure all Futures are properly handled
4. Test async operations with small values first
5. Verify correct sequence of execution for composed Futures

## Finalize Functions

```leo
// Finalize block for a transition
transition update_state(value: u32) {
    return then finalize(value);
}

finalize update_state(value: u32) {
    // Access on-chain state
    Mapping::set(value, true);
}
``` 