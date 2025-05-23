import credits.aleo;
import token_registry.aleo;
program my_arc21_token.aleo;

struct TokenMetadata:
    token_id as field;
    name as u128;
    symbol as u128;
    decimals as u8;
    supply as u128;
    max_supply as u128;
    admin as address;
    external_authorization_required as boolean;
    external_authorization_party as address;

struct TokenOwner:
    account as address;
    token_id as field;

mapping is_initialized:
    key as boolean.public;
    value as boolean.public;

function initialize:
    async initialize into r0;
    output r0 as my_arc21_token.aleo/initialize.future;

finalize initialize:
    get.or_use is_initialized[true] false into r0;
    assert.eq r0 false;
    set true into is_initialized[true];

function register_with_registry:
    call token_registry.aleo/register_token 1234567890123456789field 77121065114099050050049084111107101110u128 77065084u128 6u8 1000000000000u128 false aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc into r0;
    async register_with_registry r0 into r1;
    output r1 as my_arc21_token.aleo/register_with_registry.future;

finalize register_with_registry:
    input r0 as token_registry.aleo/register_token.future;
    get is_initialized[true] into r1;
    assert.eq r1 true;
    await r0;

function mint:
    input r0 as u128.public;
    input r1 as u32.public;
    input r2 as credits.aleo/credits.record;
    gte r1 1000u32 into r3;
    assert.eq r3 true;
    cast r0 into r4 as u64;
    mul r4 1000000u64 into r5;
    gte r2.microcredits r5 into r6;
    assert.eq r6 true;
    call credits.aleo/transfer_private r2 aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc r5 into r7 r8;
    call token_registry.aleo/mint_public 1234567890123456789field self.caller r0 4294967295u32 into r9;
    async mint r9 r1 into r10;
    output r7 as credits.aleo/credits.record;
    output r8 as credits.aleo/credits.record;
    output r10 as my_arc21_token.aleo/mint.future;

finalize mint:
    input r0 as token_registry.aleo/mint_public.future;
    input r1 as u32.public;
    get is_initialized[true] into r2;
    assert.eq r2 true;
    gte r1 1000u32 into r3;
    assert.eq r3 true;
    await r0;

function update_admin:
    input r0 as address.public;
    call token_registry.aleo/update_token_management 1234567890123456789field r0 aleo1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq3ljyzc into r1;
    async update_admin r1 into r2;
    output r2 as my_arc21_token.aleo/update_admin.future;

finalize update_admin:
    input r0 as token_registry.aleo/update_token_management.future;
    get is_initialized[true] into r1;
    assert.eq r1 true;
    await r0;

function get_token_info:
    output 1234567890123456789field as field.private;
    output 77121065114099050050049084111107101110u128 as u128.private;
    output 77065084u128 as u128.private;
    output 6u8 as u8.private;
    output 1000000000000u128 as u128.private;

function check_initialization:
    async check_initialization into r0;
    output r0 as my_arc21_token.aleo/check_initialization.future;

finalize check_initialization:
    get.or_use is_initialized[true] false into r0;
    assert.eq r0 true;
