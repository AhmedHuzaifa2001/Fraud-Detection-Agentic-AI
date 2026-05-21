# Mock geospatial database
MOCK_ADDRESSES = {
    "123 business blvd, suite 500, new york, ny": {
        "verified": True,
        "zoning_type": "Commercial",
        "is_po_box": False,
        "is_ups_store": False,
        "location_type": "Office Building",
        "coordinates": {"lat": 40.7128, "lon": -74.0060}
    },
    "p.o. box 789, miami, fl": {
        "verified": True,
        "zoning_type": "Unknown",
        "is_po_box": True,
        "is_ups_store": False,
        "location_type": "Mail Facility",
        "coordinates": None
    },

    "456 empty street, austin, tx": {
        "verified": True,
        "zoning_type": "Unknown",
        "is_po_box": False,
        "is_ups_store": False,
        "location_type": "Empty Lot",
        "coordinates": None
},


    "789 corporate drive, san francisco, ca": {
        "verified": True,
        "zoning_type": "Commercial",
        "is_po_box": False,
        "is_ups_store": False,
        "location_type": "Office Building",
        "coordinates": {"lat": 37.7749, "lon": -122.4194}
},

    "ups store #123, suite 45, las vegas, nv": {
        "verified": True,
        "zoning_type": "Unknown",
        "is_po_box": False,
        "is_ups_store": True,
        "location_type": "Mail Forwarding Service",
        "coordinates": None
}

}


def geospatial_lookup(address:str) -> dict:
    """
    Verifies physical address and detects suspicious locations.
    
    Args:
        address: Physical address to verify
        
    Returns:
        Dictionary with address verification details
    """

    print(f"Verifying the Address: {address}")

    normalized_address = address.lower().strip()

    address_data = MOCK_ADDRESSES.get(normalized_address)

    if address_data:
        return{
            "verified": True,
            "address": address,
            "zoning_type": address_data["zoning_type"],
            "is_po_box": address_data["is_po_box"],
            "is_ups_store": address_data["is_ups_store"],
            "location_type": address_data["location_type"],
            "coordinates": address_data["coordinates"]
        }
    
    else:
        return _analyze_address_patterns(address)



def _analyze_address_patterns(address: str) -> dict:
    address_lower = address.lower()
    
    # Check for P.O. Box keywords
    is_po_box = any(keyword in address_lower for keyword in 
                    ["p.o. box", "po box", "p o box", "pobox"])
    
    # Check for UPS Store / PMB keywords
    is_ups_store = any(keyword in address_lower for keyword in 
                       ["ups store", "pmb", "suite", "mailbox"])
    
    return {
        "verified": False,
        "address": address,
        "zoning_type": "Unknown",
        "is_po_box": is_po_box,
        "is_ups_store": is_ups_store,
        "location_type": "Unverified",
        "coordinates": None
    }