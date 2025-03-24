# DHL Tracking HACS Integration

Warning: This integration is still under developing!

## How to use

1. Apply for a DHL developer token with `Shipment Tracking - Unified` privilege: https://developer.dhl.com/api-reference/shipment-tracking#get-started-section/

    - Click `Try Now` button in the page to register the account and apply for the previlege. The application normally will be approved after 1-3 workdays.
    - Get the `API Key` in My app page.

2. Install the integration by HACS and then reboot the home-assistant.
3. Now you can add the new `DHL Tracking` in the integration page.
4. You need to pass three params when initializing the integration:
    - api_token: `API Key` from DHL Developer Portal
    - tracking_number: Your DHL tracking number.
    - packet_name: Name of the packet, it will be the friendly name of the entity.
