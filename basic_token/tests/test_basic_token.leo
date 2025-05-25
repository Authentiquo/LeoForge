// The 'test_basic_token' test program.
import basic_token.aleo;
program test_basic_token.aleo {
    @test
    script test_it() {
        let result: u32 = basic_token.aleo/main(1u32, 2u32);
        assert_eq(result, 3u32);
    }

    @test
    @should_fail
    transition do_nothing() {
        let result: u32 = basic_token.aleo/main(2u32, 3u32);
        assert_eq(result, 3u32);
    }
}
