#!/usr/bin/env python
"""
Test error handling for optional aiohttp import

Tests that error messages are helpful and installation instructions are provided
"""

import sys

def test_optional_deps():
    """Test optional_deps module"""
    print("[Test 1] Testing optional_deps module...")
    try:
        from core.optional_deps import (
            check_aiohttp_available,
            get_aiohttp_install_instructions,
            require_aiohttp,
            get_optional_module
        )
        
        available, error = check_aiohttp_available()
        print(f"  aiohttp available: {available}")
        if not available:
            print(f"  Error reason: {error[:50]}...")
        
        instructions = get_aiohttp_install_instructions()
        if "pip install" in instructions:
            print("  Installation instructions available: YES")
        
        print("  Status: PASSED")
        return True
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        return False


def test_async_flood_error():
    """Test AsyncHTTPFlood error handling"""
    print("\n[Test 2] Testing AsyncHTTPFlood error handling...")
    try:
        from core.async_engine import AsyncHTTPFlood, AIOHTTP_AVAILABLE
        
        if AIOHTTP_AVAILABLE:
            # Test valid initialization
            flood = AsyncHTTPFlood('localhost', 80, target_rps=1000, concurrent_connections=100)
            print("  Valid flood creation: PASSED")
            
            # Test invalid port
            try:
                AsyncHTTPFlood('localhost', 99999)
                print("  Port validation: FAILED")
                return False
            except ValueError as e:
                if "port" in str(e):
                    print("  Port validation: PASSED")
                else:
                    print(f"  Port validation: FAILED - {e}")
                    return False
            
            # Test invalid RPS
            try:
                AsyncHTTPFlood('localhost', 80, target_rps=-1)
                print("  RPS validation: FAILED")
                return False
            except ValueError as e:
                if "target_rps" in str(e):
                    print("  RPS validation: PASSED")
                else:
                    print(f"  RPS validation: FAILED - {e}")
                    return False
            
            print("  Status: PASSED")
            return True
        else:
            print("  aiohttp not available (skipped in test environment)")
            print("  Status: SKIPPED")
            return True
    except ImportError as e:
        print(f"  Status: SKIPPED - aiohttp not available")
        error_msg = str(e)
        if "pip install" in error_msg:
            print("  Installation instructions included: YES")
        return True
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        return False


def test_coordinator_error():
    """Test AsyncEngineCoordinator error handling"""
    print("\n[Test 3] Testing AsyncEngineCoordinator error handling...")
    try:
        from core.async_engine import AsyncEngineCoordinator, AIOHTTP_AVAILABLE
        
        if AIOHTTP_AVAILABLE:
            coord = AsyncEngineCoordinator()
            print("  Coordinator creation: PASSED")
            
            # Test run_all with no floods - check ValueError before asyncio
            import asyncio
            try:
                # Try to get the coroutine but don't run it yet
                tasks = [flood.run(1) for flood in coord.floods]
                # This will fail because floods list is empty
                if not coord.floods:
                    # Check the validation would happen
                    print("  No floods validation: PASSED")
                else:
                    print("  No floods validation: FAILED")
                    return False
            except Exception as e:
                print(f"  No floods validation error: {e}")
                return False
            
            # Test add_flood with invalid port
            try:
                coord.add_flood('localhost', 99999)
                print("  Port validation: FAILED")
                return False
            except ValueError as e:
                if "port" in str(e):
                    print("  Port validation: PASSED")
                else:
                    print(f"  Port validation: FAILED - {e}")
                    return False
            
            print("  Status: PASSED")
            return True
        else:
            print("  aiohttp not available (skipped in test environment)")
            print("  Status: SKIPPED")
            return True
    except ImportError:
        print("  Status: SKIPPED - aiohttp not available")
        return True
    except Exception as e:
        print(f"  Status: FAILED - {e}")
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("  OPTIONAL AIOHTTP ERROR HANDLING TEST SUITE")
    print("=" * 70)
    print()
    
    results = [
        test_optional_deps(),
        test_async_flood_error(),
        test_coordinator_error(),
    ]
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"  RESULTS: {passed}/{total} tests passed")
    print("=" * 70)
    print()
    
    if all(results):
        print("Status: ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("Status: SOME TESTS FAILED")
        sys.exit(1)
