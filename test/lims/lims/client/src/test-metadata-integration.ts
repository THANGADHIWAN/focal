/**
 * Test script to verify frontend metadata integration
 * This script tests the metadata service and context integration
 */

import API from './api';

async function testMetadataIntegration() {
    console.log('🧪 Testing Frontend Metadata Integration');
    console.log('='.repeat(50));

    try {
        // Test 1: Check service health
        console.log('\n1. Testing service health...');
        try {
            const health = await API.metadata.checkHealth();
            console.log('✅ Health check passed:', health);
        } catch (error) {
            console.log('❌ Health check failed:', error);
        }

        // Test 2: Get equipment types
        console.log('\n2. Testing equipment types...');
        try {
            const equipmentTypes = await API.metadata.getEquipmentTypes();
            console.log(`✅ Found ${equipmentTypes.length} equipment types:`);
            equipmentTypes.forEach(type => {
                console.log(`   - ${type.value} (${type.description})`);
            });
        } catch (error) {
            console.log('❌ Equipment types failed:', error);
        }

        // Test 3: Get equipment statuses
        console.log('\n3. Testing equipment statuses...');
        try {
            const equipmentStatuses = await API.metadata.getEquipmentStatuses();
            console.log(`✅ Found ${equipmentStatuses.length} equipment statuses:`);
            equipmentStatuses.forEach(status => {
                console.log(`   - ${status.value} (${status.description})`);
            });
        } catch (error) {
            console.log('❌ Equipment statuses failed:', error);
        }

        // Test 4: Get equipment
        console.log('\n4. Testing equipment retrieval...');
        try {
            const equipment = await API.metadata.getEquipment();
            console.log(`✅ Found ${equipment.length} equipment items:`);
            equipment.slice(0, 3).forEach(eq => {
                console.log(`   - ${eq.name} (${eq.instrument_type}) - ${eq.status}`);
            });
        } catch (error) {
            console.log('❌ Equipment retrieval failed:', error);
        }

        // Test 5: Get sample types
        console.log('\n5. Testing sample types...');
        try {
            const sampleTypes = await API.metadata.getSampleTypes();
            console.log(`✅ Found ${sampleTypes.length} sample types:`);
            sampleTypes.slice(0, 5).forEach(type => {
                console.log(`   - ${type.value} (${type.description})`);
            });
        } catch (error) {
            console.log('❌ Sample types failed:', error);
        }

        // Test 6: Get storage locations
        console.log('\n6. Testing storage locations...');
        try {
            const storageLocations = await API.metadata.getStorageLocations();
            console.log(`✅ Found ${storageLocations.length} storage locations:`);
            storageLocations.slice(0, 3).forEach(loc => {
                console.log(`   - ${loc.name} (${loc.description})`);
            });
        } catch (error) {
            console.log('❌ Storage locations failed:', error);
        }

        // Test 7: Get storage hierarchy
        console.log('\n7. Testing storage hierarchy...');
        try {
            const hierarchy = await API.metadata.getStorageHierarchy();
            const locationsCount = hierarchy.storage_locations.length;
            console.log(`✅ Found ${locationsCount} storage locations in hierarchy`);
            
            hierarchy.storage_locations.forEach(location => {
                console.log(`   - ${location.location_name} (${location.storage_rooms.length} rooms)`);
                location.storage_rooms.forEach(room => {
                    console.log(`     └─ ${room.room_name} (${room.freezers.length} freezers)`);
                });
            });
        } catch (error) {
            console.log('❌ Storage hierarchy failed:', error);
        }

        // Test 8: Get available slots
        console.log('\n8. Testing available slots...');
        try {
            const availableSlots = await API.metadata.getAvailableSlots();
            console.log(`✅ Found ${availableSlots.length} available slots`);
            if (availableSlots.length > 0) {
                console.log(`   First slot: ${availableSlots[0].slot_code} in ${availableSlots[0].box.box_code}`);
            }
        } catch (error) {
            console.log('❌ Available slots failed:', error);
        }

        // Test 9: Get users
        console.log('\n9. Testing users...');
        try {
            const users = await API.metadata.getUsers();
            console.log(`✅ Found ${users.length} users:`);
            users.slice(0, 3).forEach(user => {
                console.log(`   - ${user.value} (${user.email})`);
            });
        } catch (error) {
            console.log('❌ Users failed:', error);
        }

        console.log('\n' + '='.repeat(50));
        console.log('✅ Frontend metadata integration tests completed!');
        console.log('='.repeat(50));

    } catch (error) {
        console.error('❌ Integration test failed:', error);
    }
}

// Export for use in browser console
if (typeof window !== 'undefined') {
    (window as any).testMetadataIntegration = testMetadataIntegration;
}

export default testMetadataIntegration; 