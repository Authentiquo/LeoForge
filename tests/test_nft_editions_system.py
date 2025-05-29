"""
Tests for the NFT Editions System model definitions
"""

import pytest
from src.models import ProjectType, ArchitectureDesign, CodeRequirements


@pytest.fixture
def nft_editions_architecture() -> ArchitectureDesign:
    """Fixture that builds the ArchitectureDesign instance for the nft_editions_system."""
    data_structures = [
        "NFT: record with fields (owner: address, id: u64, collection_id: u64, edition: u32, metadata: field, rarity: u8) - Private NFT record representing ownership and metadata",
        "CollectionInfo: struct with fields (name: field, symbol: field, base_uri: field, max_supply: u64, editions_count: u32, is_active: bool, creator: address) - Collection metadata and configuration",
        "EditionInfo: struct with fields (name: field, metadata: field, max_supply: u64, current_supply: u64, rarity: u8, is_claimable: bool) - Edition-specific information and supply tracking",
        "ClaimSeed: struct with fields (claimer: address, collection_id: u64, block_height: u32, nonce: u64) - Seed structure for randomized claiming",
    ]

    transitions = [
        "create_collection: async transition create_collection(public name: field, public symbol: field, public base_uri: field, public max_supply: u64, public editions_count: u32) -> Future",
        "add_edition: async transition add_edition(public collection_id: u64, public edition_name: field, public metadata: field, public max_supply: u64, public rarity: u8) -> Future",
        "mint_nft: async transition mint_nft(public collection_id: u64, public edition: u32, public to: address) -> (NFT, Future)",
        "batch_mint: async transition batch_mint(public collection_id: u64, public edition: u32, public recipients: [address; 5]) -> ([NFT; 5], Future)",
        "claim_random: async transition claim_random(public collection_id: u64, public nonce: u64) -> (NFT, Future)",
        "transfer_nft: transition transfer_nft(nft: NFT, to: address) -> NFT",
        "set_edition_claimable: async transition set_edition_claimable(public collection_id: u64, public edition: u32, public is_claimable: bool) -> Future",
        "get_collection_info: async transition get_collection_info(public collection_id: u64) -> Future",
        "get_edition_info: async transition get_edition_info(public collection_id: u64, public edition: u32) -> Future",
        "update_collection_status: async transition update_collection_status(public collection_id: u64, public is_active: bool) -> Future",
    ]

    return ArchitectureDesign(
        project_name="nft_editions_system",
        project_type=ProjectType.NFT,
        description="A comprehensive NFT system with edition-based minting and random claims.",
        features=[
            "Private NFT record management",
            "Edition-based NFT minting with metadata variants",
            "Randomized claiming mechanism using verifiable randomness",
            "Collection configuration and management",
            "Public ownership tracking",
            "Admin-controlled minting permissions",
            "Batch minting capabilities",
            "Edition limits and rarity configuration",
            "Claim pool management with fair distribution",
            "Transfer functionality between users",
            "Metadata URI management",
            "Edition enumeration and querying",
        ],
        technical_requirements=[],
        data_structures=data_structures,
        transitions=transitions,
        security_considerations=[
            "Ensure randomness source is verifiable and unbiased",
            "Protect private NFT data from unauthorized access",
        ],
        admin_features=["Admin-controlled minting permissions"],
        requires_admin=True,
    )


def test_nft_editions_architecture(nft_editions_architecture: ArchitectureDesign):
    """Basic sanity checks for the nft_editions_system ArchitectureDesign."""
    arch = nft_editions_architecture

    # Core assertions
    assert arch.project_name == "nft_editions_system"
    assert arch.project_type == ProjectType.NFT

    # Ensure key data structure definitions exist
    data_structure_names = [ds.split(":")[0].strip() for ds in arch.data_structures]
    for required_ds in ["NFT", "CollectionInfo", "EditionInfo", "ClaimSeed"]:
        assert required_ds in data_structure_names

    # There should be at least 10 features defined
    assert len(arch.features) >= 10

    # Validate that all transitions are recorded with their signatures
    expected_transitions = {
        "create_collection",
        "add_edition",
        "mint_nft",
        "batch_mint",
        "claim_random",
        "transfer_nft",
        "set_edition_claimable",
        "get_collection_info",
        "get_edition_info",
        "update_collection_status",
    }
    transition_names = {transition.split(":")[0].strip() for transition in arch.transitions}
    assert expected_transitions == transition_names

    # Security considerations should not be empty when admin is required
    assert arch.requires_admin is True
    assert len(arch.security_considerations) > 0


def test_code_requirements_creation(nft_editions_architecture: ArchitectureDesign):
    """Test creation of CodeRequirements with the given architecture design."""
    code_req = CodeRequirements(
        project_name=nft_editions_architecture.project_name,
        description=nft_editions_architecture.description,
        features=nft_editions_architecture.features,
        architecture=nft_editions_architecture,
    )

    assert code_req.project_name == "nft_editions_system"
    assert code_req.architecture.project_type == ProjectType.NFT
    assert code_req.version == "1.0.0"

    # Consistency checks
    assert code_req.features == nft_editions_architecture.features
    # Check that mint_nft transition contains "async transition"
    mint_nft_transition = next((t for t in code_req.architecture.transitions if t.startswith("mint_nft")), None)
    assert mint_nft_transition is not None
    assert "async transition" in mint_nft_transition


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 