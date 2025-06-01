// The 'test_simple_nft' test program.
import simple_nft.aleo;
program test_simple_nft.aleo {
    @test
    script test_it() {
        let result: u32 = simple_nft.aleo/main(1u32, 2u32);
        assert_eq(result, 3u32);
    }

    @test
    @should_fail
    transition do_nothing() {
        let result: u32 = simple_nft.aleo/main(2u32, 3u32);
        assert_eq(result, 3u32);
    }
}
