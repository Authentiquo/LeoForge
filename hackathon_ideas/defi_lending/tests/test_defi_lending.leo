// The 'test_defi_lending' test program.
import defi_lending.aleo;
program test_defi_lending.aleo {
    @test
    script test_it() {
        let result: u32 = defi_lending.aleo/main(1u32, 2u32);
        assert_eq(result, 3u32);
    }

    @test
    @should_fail
    transition do_nothing() {
        let result: u32 = defi_lending.aleo/main(2u32, 3u32);
        assert_eq(result, 3u32);
    }
}
