"""
Seed Integration Contracts

Creates initial integration contracts for the current system modules
and integrations that exist in Primal Genesis Engine.
"""

from .contracts import IntegrationContract
from .contract_registry import get_integration_contract_registry


def create_seed_contracts() -> list[IntegrationContract]:
    """
    Create seed contracts for current known system integrations.
    
    Returns:
        List of seed integration contracts
    """
    contracts = []
    
    # Primal Genesis Engine Core
    contracts.append(IntegrationContract(
        name="primal_genesis",
        integration_type="core",
        description="Primal Genesis Engine core system providing registry, policy, memory, and runtime services",
        version="1.0.0",
        enabled=True,
        entrypoint="packages.primal_genesis.core",
        capabilities=[
            "manage_registry",
            "enforce_policy", 
            "store_memory",
            "execute_runtime",
            "observe_system",
            "expose_api"
        ],
        status="active",
        read_only=False,
        ui_surface=None
    ))
    
    # Console Integration
    contracts.append(IntegrationContract(
        name="console",
        integration_type="ui",
        description="Web-based console for system monitoring, configuration, and interaction",
        version="1.0.0",
        enabled=True,
        entrypoint="apps.console",
        capabilities=[
            "display_console",
            "observe_system",
            "monitor_modules",
            "view_policies",
            "browse_memory"
        ],
        status="active",
        read_only=True,
        ui_surface="/console"
    ))
    
    # Override Core System
    contracts.append(IntegrationContract(
        name="override-core",
        integration_type="core",
        description="Override system for managing configuration overrides and system modifications",
        version="1.0.0",
        enabled=True,
        entrypoint="packages.primal_genesis.core.override",
        capabilities=[
            "manage_overrides",
            "modify_configuration",
            "persist_changes",
            "validate_rules"
        ],
        status="active",
        read_only=False,
        ui_surface=None
    ))
    
    # PGE Runner
    contracts.append(IntegrationContract(
        name="pge-runner",
        integration_type="executor",
        description="Primal Genesis Engine runner for executing commands and managing system lifecycle",
        version="1.0.0",
        enabled=True,
        entrypoint="packages.primal_genesis.runner",
        capabilities=[
            "run_local_simulation",
            "execute_commands",
            "manage_lifecycle",
            "handle_errors",
            "log_activity"
        ],
        status="active",
        read_only=False,
        ui_surface=None
    ))
    
    # Athena Observer System
    contracts.append(IntegrationContract(
        name="athena",
        integration_type="observer",
        description="Athena observer system for system analysis, insight generation, and intelligent monitoring",
        version="1.0.0",
        enabled=True,
        entrypoint="packages.primal_genesis.athena",
        capabilities=[
            "observe_system",
            "analyze_activity",
            "generate_insights",
            "monitor_trends",
            "provide_recommendations"
        ],
        status="active",
        read_only=True,
        ui_surface="/console/athena"
    ))
    
    return contracts


def seed_integration_contracts() -> None:
    """
    Seed the integration contract registry with initial contracts.
    
    Creates and registers the initial set of integration contracts
    representing the current system state.
    """
    registry = get_integration_contract_registry()
    
    # Only seed if registry is empty
    if not registry.list_contracts():
        contracts = create_seed_contracts()
        
        for contract in contracts:
            registry.register(contract)
        
        print(f"Seeded {len(contracts)} integration contracts")
    else:
        print("Integration contracts already exist, skipping seeding")


if __name__ == "__main__":
    # Seed contracts when run directly
    seed_integration_contracts()
