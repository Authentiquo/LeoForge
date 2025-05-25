# Leo/Aleo Developer Cheat Sheet - Complete Reference

This comprehensive cheat sheet provides ready-to-use Leo/Aleo patterns for AI code generation. Each pattern includes correct syntax, common use cases, and best practices.

---

## Table of Contents

- [1. Basic Program Structure](#1-basic-program-structure)
- [2. Types & Variables](#2-types--variables)
- [3. Data Structures](#3-data-structures)
- [4. Transitions & Functions](#4-transitions--functions)
- [5. Mappings & State Management](#5-mappings--state-management)
- [6. Control Flow](#6-control-flow)
- [7. Operators & Built-ins](#7-operators--built-ins)
- [8. Privacy & Visibility](#8-privacy--visibility)
- [9. Token Standards (ARC20/ARC721)](#9-token-standards-arc20arc721)
- [10. Common Patterns](#10-common-patterns)
- [11. Error Handling & Validation](#11-error-handling--validation)
- [12. Testing](#12-testing)
- [13. Import & Composability](#13-import--composability)
- [14. Advanced Patterns](#14-advanced-patterns)
- [15. Best Practices](#15-best-practices)

---

## 1. Basic Program Structure

### Minimal Program Template
```leo
program my_program.aleo {
    // Constants (optional)
    const MAX_VALUE: u64 = 1000u64;
    
    // Structs (optional)
    struct MyData {
        value: u64,
        owner: address,
    }
    
    // Records (optional)
    record MyRecord {
        owner: address,
        data: u64,
    }
    
    // Mappings (optional)
    mapping my_mapping: address => u64;
    
    // Transitions (required - at least one)
    transition main(input: u64) -> u64 {
        return input + 1u64;
    }
}
```

### Project Structure
```
my_project/
├── src/
│   └── main.leo          # Main program file
├── inputs/
│   └── my_program.in     # Test inputs
├── program.json          # Program metadata
└── README.md
```

---

## 2. Types & Variables

### Primitive Types
```leo
// Unsigned integers
let a: u8 = 255u8;
let b: u16 = 65535u16;
let c: u32 = 4294967295u32;
let d: u64 = 18446744073709551615u64;
let e: u128 = 340282366920938463463374607431768211455u128;

// Signed integers
let f: i8 = -128i8;
let g: i16 = -32768i16;
let h: i32 = -2147483648i32;
let i: i64 = -9223372036854775808i64;
let j: i128 = -170141183460469231731687303715884105728i128;

// Field elements (for ZK proofs)
let field_val: field = 123456789field;

// Boolean
let flag: bool = true;

// Address (Aleo account/program identifier)
let addr: address = aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8;

// Group (elliptic curve point)
let group_val: group = 1group;

// Scalar (for signatures/private keys)
let scalar_val: scalar = 1scalar;

// Arrays (fixed size)
let arr: [u32; 5] = [1u32, 2u32, 3u32, 4u32, 5u32];
```

### Variable Declaration Patterns
```leo
// Basic declaration
let x: u32 = 42u32;

// Constants (global scope)
const MAX_SUPPLY: u64 = 1000000u64;

// Type inference (when possible)
let y = 42u32; // Type inferred as u32

// Mutable variables (rare in Leo)
let mut counter: u32 = 0u32;
counter += 1u32;
```

### Type Casting
```leo
let a: u16 = 42u16;
let b: u32 = a as u32;
let c: u64 = b as u64;

// Field to group conversion
let f: field = 123field;
let g: group = f as group;
```

---

## 3. Data Structures

### Structs (Value Types)
```leo
// Basic struct
struct Point {
    x: u32,
    y: u32,
}

// Complex struct with multiple types
struct TokenInfo {
    name: field,
    symbol: field,
    decimals: u8,
    total_supply: u64,
    is_active: bool,
}

// Creating struct instances
let point: Point = Point {
    x: 10u32,
    y: 20u32,
};

let token: TokenInfo = TokenInfo {
    name: 123456field, // Encoded string
    symbol: 789field,
    decimals: 18u8,
    total_supply: 1000000u64,
    is_active: true,
};
```

### Records (Private State)
```leo
// Basic record (must have owner field)
record Token {
    owner: address,
    amount: u64,
}

// Complex record
record NFT {
    owner: address,
    id: u64,
    metadata: [field; 4], // URI or metadata hash
    edition: scalar,
}

// Creating records in transitions
transition mint_token(to: address, amount: u64) -> Token {
    return Token {
        owner: to,
        amount: amount,
    };
}
```

### Arrays (Fixed Size)
```leo
// Basic arrays
let numbers: [u32; 5] = [1u32, 2u32, 3u32, 4u32, 5u32];
let addresses: [address; 3] = [
    aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
    aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
    aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
];

// Array access
let first: u32 = numbers[0u32];
let second: u32 = numbers[1u32];

// Array iteration
for i: u32 in 0u32..5u32 {
    let value: u32 = numbers[i];
    // Process value
}
```

---

## 4. Transitions & Functions

### Basic Transitions
```leo
// Simple transition
transition add(a: u32, b: u32) -> u32 {
    return a + b;
}

// Multiple inputs and outputs
transition swap(a: u32, b: u32) -> (u32, u32) {
    return (b, a);
}

// Record consumption and creation
transition transfer(token: Token, to: address, amount: u64) -> (Token, Token) {
    // Validate ownership
    assert_eq(token.owner, self.signer);
    assert(amount <= token.amount);
    
    // Create new records
    let recipient_token: Token = Token {
        owner: to,
        amount: amount,
    };
    
    let sender_token: Token = Token {
        owner: self.signer,
        amount: token.amount - amount,
    };
    
    return (recipient_token, sender_token);
}
```

### Async Transitions (with Finalize)
```leo
// Async transition for mapping operations
async transition transfer_public(to: address, amount: u64) -> Future {
    let fut: Future = finalize_transfer_public(self.caller, to, amount);
    return fut;
}

// Corresponding finalize function
async function finalize_transfer_public(from: address, to: address, amount: u64) {
    // Get current balances
    let from_balance: u64 = Mapping::get(balances, from);
    let to_balance: u64 = Mapping::get_or_use(balances, to, 0u64);
    
    // Validate transfer
    assert(from_balance >= amount);
    
    // Update balances
    Mapping::set(balances, from, from_balance - amount);
    Mapping::set(balances, to, to_balance + amount);
}
```

### Inline Functions
```leo
// Inline function for reusable logic
inline function calculate_fee(amount: u64, rate: u64) -> u64 {
    return amount * rate / 10000u64; // Basis points
}

// Using inline function
transition transfer_with_fee(token: Token, to: address, amount: u64) -> (Token, Token) {
    let fee: u64 = calculate_fee(amount, 100u64); // 1% fee
    let net_amount: u64 = amount - fee;
    
    // ... rest of transfer logic
}
```

---

## 5. Mappings & State Management

### Mapping Declarations
```leo
// Basic mappings
mapping balances: address => u64;
mapping allowances: field => u64; // field = hash(owner, spender)
mapping token_owners: u64 => address; // NFT ID to owner
mapping settings: u8 => field; // Configuration settings

// Complex value types
mapping user_data: address => UserInfo;
mapping orders: field => OrderData;
```

### Mapping Operations (in Finalize)
```leo
async function finalize_example(user: address, amount: u64) {
    // Get value (fails if key doesn't exist)
    let balance: u64 = Mapping::get(balances, user);
    
    // Get value with default
    let balance_safe: u64 = Mapping::get_or_use(balances, user, 0u64);
    
    // Set value
    Mapping::set(balances, user, balance_safe + amount);
    
    // Check if key exists
    let exists: bool = Mapping::contains(balances, user);
    
    // Remove key-value pair
    Mapping::remove(balances, user);
}
```

### State Management Patterns
```leo
// Counter pattern
mapping counter: u8 => u64;

async function increment_counter() {
    let current: u64 = Mapping::get_or_use(counter, 0u8, 0u64);
    Mapping::set(counter, 0u8, current + 1u64);
}

// Multi-key pattern (using hash)
struct ApprovalKey {
    owner: address,
    spender: address,
}

async function set_approval(owner: address, spender: address, amount: u64) {
    let key: ApprovalKey = ApprovalKey { owner, spender };
    let key_hash: field = BHP256::hash_to_field(key);
    Mapping::set(allowances, key_hash, amount);
}
```

---

## 6. Control Flow

### Conditional Statements
```leo
// Basic if-else
if amount > 0u64 {
    // Process positive amount
} else {
    // Handle zero or invalid amount
}

// Multiple conditions
if amount > 1000u64 {
    // Large amount
} else if amount > 100u64 {
    // Medium amount
} else if amount > 0u64 {
    // Small amount
} else {
    // Invalid amount
}

// Ternary operator
let fee: u64 = is_premium ? 0u64 : calculate_fee(amount);
```

### Loops
```leo
// For loop with fixed range
for i: u32 in 0u32..10u32 {
    // Process index i (0 to 9)
}

// Array iteration
let arr: [u32; 5] = [1u32, 2u32, 3u32, 4u32, 5u32];
for i: u32 in 0u32..5u32 {
    let value: u32 = arr[i];
    // Process value
}

// Nested loops
for i: u32 in 0u32..3u32 {
    for j: u32 in 0u32..3u32 {
        // Process i, j
    }
}
```

---

## 7. Operators & Built-ins

### Arithmetic Operators
```leo
let a: u64 = 10u64;
let b: u64 = 3u64;

let sum: u64 = a + b;        // Addition: 13
let diff: u64 = a - b;       // Subtraction: 7
let product: u64 = a * b;    // Multiplication: 30
let quotient: u64 = a / b;   // Division: 3
let remainder: u64 = a % b;  // Modulo: 1
let power: u64 = a.pow(2u32); // Exponentiation: 100

// Compound assignment
let mut x: u64 = 10u64;
x += 5u64;  // x = 15
x -= 3u64;  // x = 12
x *= 2u64;  // x = 24
x /= 4u64;  // x = 6
```

### Comparison Operators
```leo
let a: u64 = 10u64;
let b: u64 = 20u64;

let eq: bool = a == b;  // false
let ne: bool = a != b;  // true
let lt: bool = a < b;   // true
let le: bool = a <= b;  // true
let gt: bool = a > b;   // false
let ge: bool = a >= b;  // false
```

### Logical Operators
```leo
let a: bool = true;
let b: bool = false;

let and_result: bool = a && b;  // false
let or_result: bool = a || b;   // true
let not_result: bool = !a;      // false
```

### Bitwise Operators
```leo
let a: u8 = 0b1100u8;  // 12
let b: u8 = 0b1010u8;  // 10

let and_bits: u8 = a & b;      // 0b1000 = 8
let or_bits: u8 = a | b;       // 0b1110 = 14
let xor_bits: u8 = a ^ b;      // 0b0110 = 6
let not_bits: u8 = !a;         // 0b11110011 = 243
let left_shift: u8 = a << 1u32; // 0b11000 = 24
let right_shift: u8 = a >> 1u32; // 0b0110 = 6
```

### Hash Functions
```leo
// BHP256 hash to field
let hash: field = BHP256::hash_to_field(value1, value2);

// BHP256 hash to different types
let hash_u8: u8 = BHP256::hash_to_u8(value);
let hash_u16: u16 = BHP256::hash_to_u16(value);
let hash_u32: u32 = BHP256::hash_to_u32(value);
let hash_u64: u64 = BHP256::hash_to_u64(value);
let hash_u128: u128 = BHP256::hash_to_u128(value);

// BHP512 variants
let hash_512: field = BHP512::hash_to_field(value);

// Commitment (hash with randomness)
let commit: field = BHP256::commit_to_field(value, randomness);
```

### Context Access
```leo
transition example() {
    let signer: address = self.signer;  // Transaction signer
    let caller: address = self.caller;  // Direct caller (for composability)
}

async function finalize_example() {
    let height: u32 = block.height;  // Current block height
}
```

---

## 8. Privacy & Visibility

### Public vs Private
```leo
// All private by default
transition private_example(a: u64, b: u64) -> u64 {
    return a + b;
}

// Explicit public inputs/outputs
transition public_example(public a: u64, private b: u64) -> (public u64, private u64) {
    return (a + b, a - b);
}

// Mixed visibility
transition mixed_example(
    public recipient: address,
    private amount: u64,
    token: Token
) -> (public bool, Token) {
    // Transfer logic
    let new_token: Token = Token {
        owner: recipient,
        amount: amount,
    };
    return (true, new_token);
}
```

### Record Privacy
```leo
// Records are always private
record PrivateToken {
    owner: address,      // Private
    amount: u64,         // Private
    metadata: field,     // Private
}

// Converting private to public
async transition private_to_public(token: PrivateToken) -> Future {
    let fut: Future = finalize_private_to_public(token.owner, token.amount);
    return fut;
}

async function finalize_private_to_public(owner: address, amount: u64) {
    let current: u64 = Mapping::get_or_use(public_balances, owner, 0u64);
    Mapping::set(public_balances, owner, current + amount);
}
```

---

## 9. Token Standards (ARC20/ARC721)

### ARC20 Fungible Token
```leo
program token.aleo {
    // Token record for private transfers
    record Token {
        owner: address,
        amount: u64,
    }
    
    // Public balances mapping
    mapping account: address => u64;
    
    // Allowances for delegated transfers
    mapping allowances: field => u64;
    
    // Token metadata
    struct TokenInfo {
        name: field,
        symbol: field,
        decimals: u8,
        total_supply: u64,
    }
    
    mapping token_info: u8 => TokenInfo;
    
    // Initialize token
    async transition initialize(
        public name: field,
        public symbol: field,
        public decimals: u8,
        public total_supply: u64
    ) -> (Token, Future) {
        let token: Token = Token {
            owner: self.caller,
            amount: total_supply,
        };
        
        let fut: Future = finalize_initialize(name, symbol, decimals, total_supply);
        return (token, fut);
    }
    
    async function finalize_initialize(
        name: field,
        symbol: field,
        decimals: u8,
        total_supply: u64
    ) {
        let info: TokenInfo = TokenInfo {
            name,
            symbol,
            decimals,
            total_supply,
        };
        Mapping::set(token_info, 0u8, info);
    }
    
    // Private transfer
    transition transfer_private(
        token: Token,
        to: address,
        amount: u64
    ) -> (Token, Token) {
        assert_eq(token.owner, self.caller);
        assert(amount <= token.amount);
        
        let recipient_token: Token = Token {
            owner: to,
            amount: amount,
        };
        
        let sender_token: Token = Token {
            owner: self.caller,
            amount: token.amount - amount,
        };
        
        return (recipient_token, sender_token);
    }
    
    // Public transfer
    async transition transfer_public(
        public to: address,
        public amount: u64
    ) -> Future {
        let fut: Future = finalize_transfer_public(self.caller, to, amount);
        return fut;
    }
    
    async function finalize_transfer_public(
        from: address,
        to: address,
        amount: u64
    ) {
        let from_balance: u64 = Mapping::get(account, from);
        assert(from_balance >= amount);
        
        let to_balance: u64 = Mapping::get_or_use(account, to, 0u64);
        
        Mapping::set(account, from, from_balance - amount);
        Mapping::set(account, to, to_balance + amount);
    }
}
```

### ARC721 NFT
```leo
program nft.aleo {
    // NFT record
    record NFT {
        owner: address,
        id: u64,
        metadata: [field; 4],
        edition: scalar,
    }
    
    // Public ownership tracking
    mapping nft_owners: u64 => address;
    mapping nft_exists: u64 => bool;
    
    // Collection info
    mapping collection_info: u8 => CollectionInfo;
    mapping next_token_id: u8 => u64;
    
    struct CollectionInfo {
        name: field,
        symbol: field,
        base_uri: [field; 4],
        total_supply: u64,
        max_supply: u64,
    }
    
    // Mint NFT
    async transition mint(
        public to: address,
        public metadata: [field; 4]
    ) -> (NFT, Future) {
        let nft: NFT = NFT {
            owner: to,
            id: 0u64, // Will be set in finalize
            metadata,
            edition: 1scalar,
        };
        
        let fut: Future = finalize_mint(to, metadata);
        return (nft, fut);
    }
    
    async function finalize_mint(to: address, metadata: [field; 4]) {
        let token_id: u64 = Mapping::get_or_use(next_token_id, 0u8, 1u64);
        
        Mapping::set(nft_owners, token_id, to);
        Mapping::set(nft_exists, token_id, true);
        Mapping::set(next_token_id, 0u8, token_id + 1u64);
    }
}
```

---

## 10. Common Patterns

### Access Control
```leo
// Owner-only modifier pattern
const OWNER: address = aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8;

transition only_owner() {
    assert_eq(self.caller, OWNER);
    // Owner-only logic
}

// Role-based access control
mapping roles: address => u8;
const ADMIN_ROLE: u8 = 1u8;
const MINTER_ROLE: u8 = 2u8;

async transition set_role(public user: address, public role: u8) -> Future {
    assert_eq(self.caller, OWNER);
    let fut: Future = finalize_set_role(user, role);
    return fut;
}

async function finalize_set_role(user: address, role: u8) {
    Mapping::set(roles, user, role);
}

async transition mint_with_role(public to: address, public amount: u64) -> Future {
    let fut: Future = finalize_mint_with_role(self.caller, to, amount);
    return fut;
}

async function finalize_mint_with_role(caller: address, to: address, amount: u64) {
    let caller_role: u8 = Mapping::get(roles, caller);
    assert(caller_role == ADMIN_ROLE || caller_role == MINTER_ROLE);
    
    // Mint logic
    let balance: u64 = Mapping::get_or_use(balances, to, 0u64);
    Mapping::set(balances, to, balance + amount);
}
```

### Pausable Contract
```leo
mapping is_paused: u8 => bool;

async transition pause() -> Future {
    assert_eq(self.caller, OWNER);
    let fut: Future = finalize_pause();
    return fut;
}

async function finalize_pause() {
    Mapping::set(is_paused, 0u8, true);
}

async transition unpause() -> Future {
    assert_eq(self.caller, OWNER);
    let fut: Future = finalize_unpause();
    return fut;
}

async function finalize_unpause() {
    Mapping::set(is_paused, 0u8, false);
}

// Use in other functions
async function finalize_transfer(from: address, to: address, amount: u64) {
    let paused: bool = Mapping::get_or_use(is_paused, 0u8, false);
    assert(!paused);
    
    // Transfer logic
}
```

### Escrow Pattern
```leo
record EscrowDeposit {
    depositor: address,
    beneficiary: address,
    amount: u64,
    release_height: u32,
}

transition create_escrow(
    beneficiary: address,
    amount: u64,
    lock_duration: u32
) -> EscrowDeposit {
    return EscrowDeposit {
        depositor: self.caller,
        beneficiary,
        amount,
        release_height: 0u32, // Set in finalize
    };
}

async transition release_escrow(deposit: EscrowDeposit) -> (Token, Future) {
    let token: Token = Token {
        owner: deposit.beneficiary,
        amount: deposit.amount,
    };
    
    let fut: Future = finalize_release_escrow(deposit.release_height);
    return (token, fut);
}

async function finalize_release_escrow(release_height: u32) {
    assert(block.height >= release_height);
}
```

### Multi-signature Pattern
```leo
struct MultiSigProposal {
    id: u64,
    target: address,
    amount: u64,
    approvals: u8,
    executed: bool,
}

mapping proposals: u64 => MultiSigProposal;
mapping has_approved: field => bool; // hash(proposal_id, signer)
mapping signers: address => bool;
mapping proposal_count: u8 => u64;

const REQUIRED_APPROVALS: u8 = 3u8;

async transition propose(
    public target: address,
    public amount: u64
) -> Future {
    let fut: Future = finalize_propose(self.caller, target, amount);
    return fut;
}

async function finalize_propose(proposer: address, target: address, amount: u64) {
    let is_signer: bool = Mapping::get(signers, proposer);
    assert(is_signer);
    
    let proposal_id: u64 = Mapping::get_or_use(proposal_count, 0u8, 0u64);
    let proposal: MultiSigProposal = MultiSigProposal {
        id: proposal_id,
        target,
        amount,
        approvals: 0u8,
        executed: false,
    };
    
    Mapping::set(proposals, proposal_id, proposal);
    Mapping::set(proposal_count, 0u8, proposal_id + 1u64);
}
```

---

## 11. Error Handling & Validation

### Assertions
```leo
// Basic assertions
assert(amount > 0u64);
assert_eq(token.owner, self.caller);
assert_neq(recipient, self.caller);

// Custom error messages (via comments)
assert(amount > 0u64); // Amount must be positive
assert_eq(token.owner, self.caller); // Only token owner can transfer
```

### Input Validation
```leo
transition transfer(token: Token, to: address, amount: u64) -> (Token, Token) {
    // Validate ownership
    assert_eq(token.owner, self.caller);
    
    // Validate amount
    assert(amount > 0u64);
    assert(amount <= token.amount);
    
    // Validate recipient
    assert_neq(to, self.caller); // Can't transfer to self
    
    // Transfer logic...
}
```

### Overflow Protection
```leo
transition safe_add(a: u64, b: u64) -> u64 {
    // Check for overflow
    assert(a <= u64::MAX - b);
    return a + b;
}

transition safe_multiply(a: u64, b: u64) -> u64 {
    if a == 0u64 || b == 0u64 {
        return 0u64;
    }
    
    // Check for overflow
    assert(a <= u64::MAX / b);
    return a * b;
}
```

---

## 12. Testing

### Basic Tests
```leo
// Test file: tests/test_basic.leo
test test_addition() {
    let result: u32 = add(2u32, 3u32);
    assert_eq(result, 5u32);
}

test test_transfer() {
    let token: Token = Token {
        owner: aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
        amount: 100u64,
    };
    
    let (recipient_token, sender_token): (Token, Token) = transfer_private(
        token,
        aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
        30u64
    );
    
    assert_eq(recipient_token.amount, 30u64);
    assert_eq(sender_token.amount, 70u64);
}
```

### Test Input Files
```
// inputs/token.in
[main]
token: Token = Token {
    owner: aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
    amount: 100u64
};
to: address = aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8;
amount: u64 = 30u64;
```

---

## 13. Import & Composability

### Importing Programs
```leo
// Import external program
import token.aleo;
import nft.aleo;

// Use imported functions
transition use_external() -> u64 {
    let result: u64 = token.aleo/get_balance(self.caller);
    return result;
}

// Use imported records
transition use_external_record(token: token.aleo/Token) -> token.aleo/Token {
    return token.aleo/transfer_private(token, self.caller, 10u64);
}
```

### Cross-Program Communication
```leo
// Program A calls Program B
import program_b.aleo;

async transition call_external(amount: u64) -> Future {
    let fut: Future = program_b.aleo/process_payment(self.caller, amount);
    return fut;
}

// Chaining futures
async transition complex_operation() -> Future {
    let fut1: Future = program_b.aleo/step_one();
    let fut2: Future = program_c.aleo/step_two();
    let fut: Future = finalize_complex_operation(fut1, fut2);
    return fut;
}

async function finalize_complex_operation(fut1: Future, fut2: Future) {
    fut1.await();
    fut2.await();
    // Additional logic
}
```

---

## 14. Advanced Patterns

### State Machines
```leo
// State enumeration using u8
const STATE_PENDING: u8 = 0u8;
const STATE_ACTIVE: u8 = 1u8;
const STATE_COMPLETED: u8 = 2u8;
const STATE_CANCELLED: u8 = 3u8;

mapping contract_state: u8 => u8;

async transition activate() -> Future {
    let fut: Future = finalize_activate();
    return fut;
}

async function finalize_activate() {
    let current_state: u8 = Mapping::get_or_use(contract_state, 0u8, STATE_PENDING);
    assert_eq(current_state, STATE_PENDING);
    Mapping::set(contract_state, 0u8, STATE_ACTIVE);
}
```

### Batch Operations
```leo
// Batch transfer using arrays
transition batch_transfer(
    tokens: [Token; 5],
    recipients: [address; 5],
    amounts: [u64; 5]
) -> [Token; 10] {
    let mut result_tokens: [Token; 10] = [Token {
        owner: aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8,
        amount: 0u64,
    }; 10];
    
    for i: u32 in 0u32..5u32 {
        let (recipient_token, sender_token): (Token, Token) = transfer_private(
            tokens[i],
            recipients[i],
            amounts[i]
        );
        result_tokens[i] = recipient_token;
        result_tokens[i + 5u32] = sender_token;
    }
    
    return result_tokens;
}
```

### Time-locked Operations
```leo
mapping time_locks: address => u32;

async transition create_time_lock(public duration: u32) -> Future {
    let fut: Future = finalize_create_time_lock(self.caller, duration);
    return fut;
}

async function finalize_create_time_lock(user: address, duration: u32) {
    let unlock_height: u32 = block.height + duration;
    Mapping::set(time_locks, user, unlock_height);
}

async transition unlock() -> Future {
    let fut: Future = finalize_unlock(self.caller);
    return fut;
}

async function finalize_unlock(user: address) {
    let unlock_height: u32 = Mapping::get(time_locks, user);
    assert(block.height >= unlock_height);
    Mapping::remove(time_locks, user);
}
```

---

## 15. Best Practices

### Code Organization
```leo
program my_program.aleo {
    // 1. Constants first
    const MAX_SUPPLY: u64 = 1000000u64;
    const OWNER: address = aleo1qnr4dkkvkgfqph0vzc3y6z2eu975wnpz2925ntjccd5cfqxtyu8sta57j8;
    
    // 2. Structs
    struct TokenInfo {
        name: field,
        symbol: field,
        decimals: u8,
    }
    
    // 3. Records
    record Token {
        owner: address,
        amount: u64,
    }
    
    // 4. Mappings
    mapping balances: address => u64;
    
    // 5. Inline functions
    inline function calculate_fee(amount: u64) -> u64 {
        return amount / 100u64; // 1% fee
    }
    
    // 6. Transitions (public interface first)
    transition transfer(token: Token, to: address, amount: u64) -> (Token, Token) {
        // Implementation
    }
    
    // 7. Async transitions
    async transition transfer_public(to: address, amount: u64) -> Future {
        // Implementation
    }
    
    // 8. Finalize functions
    async function finalize_transfer_public(from: address, to: address, amount: u64) {
        // Implementation
    }
}
```

### Security Checklist
```leo
// ✅ Always validate inputs
assert(amount > 0u64);
assert_eq(token.owner, self.caller);

// ✅ Check for overflows
assert(balance + amount >= balance);

// ✅ Validate addresses
assert_neq(to, self.caller);

// ✅ Use proper access control
assert_eq(self.caller, OWNER);

// ✅ Handle edge cases
if amount == 0u64 {
    return token; // No-op for zero amount
}

// ✅ Use safe arithmetic
inline function safe_add(a: u64, b: u64) -> u64 {
    assert(a <= u64::MAX - b);
    return a + b;
}
```

### Performance Tips
```leo
// ✅ Use inline functions for small utilities
inline function min(a: u64, b: u64) -> u64 {
    return a < b ? a : b;
}

// ✅ Minimize mapping operations
async function finalize_batch_update(users: [address; 10], amounts: [u64; 10]) {
    for i: u32 in 0u32..10u32 {
        let balance: u64 = Mapping::get_or_use(balances, users[i], 0u64);
        Mapping::set(balances, users[i], balance + amounts[i]);
    }
}

// ✅ Use appropriate data types
let small_number: u8 = 255u8;    // Use u8 for small values
let large_number: u128 = 1000000000000000000u128; // Use u128 for large values

// ✅ Batch operations when possible
transition batch_mint(recipients: [address; 5], amounts: [u64; 5]) -> [Token; 5] {
    // Process multiple operations in one transition
}
```

### Common Mistakes to Avoid
```leo
// ❌ Don't forget to validate ownership
transition bad_transfer(token: Token, to: address) -> Token {
    // Missing: assert_eq(token.owner, self.caller);
    return Token { owner: to, amount: token.amount };
}

// ✅ Always validate ownership
transition good_transfer(token: Token, to: address) -> Token {
    assert_eq(token.owner, self.caller);
    return Token { owner: to, amount: token.amount };
}

// ❌ Don't use mappings in transitions
transition bad_get_balance(user: address) -> u64 {
    // This won't work - mappings only in finalize
    return Mapping::get(balances, user);
}

// ✅ Use async transition + finalize for mappings
async transition good_get_balance(public user: address) -> Future {
    let fut: Future = finalize_get_balance(user);
    return fut;
}

async function finalize_get_balance(user: address) {
    let balance: u64 = Mapping::get_or_use(balances, user, 0u64);
    // Process balance
}

// ❌ Don't forget overflow checks
transition bad_add(a: u64, b: u64) -> u64 {
    return a + b; // Could overflow
}

// ✅ Check for overflows
transition good_add(a: u64, b: u64) -> u64 {
    assert(a <= u64::MAX - b);
    return a + b;
}
```

---

## Quick Reference

### Essential Syntax
```leo
// Program declaration
program name.aleo { }

// Constants
const NAME: type = value;

// Structs
struct Name { field: type }

// Records
record Name { owner: address, field: type }

// Mappings
mapping name: key_type => value_type;

// Transitions
transition name(param: type) -> return_type { }

// Async transitions
async transition name() -> Future { }

// Finalize functions
async function finalize_name() { }

// Inline functions
inline function name() -> type { }
```

### Common Types
- `u8, u16, u32, u64, u128` - Unsigned integers
- `i8, i16, i32, i64, i128` - Signed integers
- `field` - Field element
- `bool` - Boolean
- `address` - Aleo address
- `group` - Group element
- `scalar` - Scalar element
- `[T; N]` - Array of N elements of type T

### Key Functions
- `assert(condition)` - Assert condition is true
- `assert_eq(a, b)` - Assert equality
- `assert_neq(a, b)` - Assert inequality
- `BHP256::hash_to_field(...)` - Hash to field
- `Mapping::get(map, key)` - Get mapping value
- `Mapping::set(map, key, value)` - Set mapping value
- `Mapping::get_or_use(map, key, default)` - Get with default
- `self.caller` - Transaction caller
- `self.signer` - Transaction signer
- `block.height` - Current block height (in finalize)

This cheat sheet provides comprehensive patterns and examples for Leo/Aleo development, covering everything from basic syntax to advanced patterns and best practices. 