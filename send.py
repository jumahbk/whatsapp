from heyoo import WhatsApp
messenger = WhatsApp('EAAHlPsvlZAjABAOEfd1bBtf5ZBDtxyquQ0rCL7MxfN4OZADYWdpScUTyKVwM6pd99QhIKE07uim2FKhJnAgmNERCO2s5c03iM7HLJQooXphqi0eYgjJCOeKazjGtZCngW124oVQ7aPIuYBfyJt1vOoNagvCx0HOQZB0zkf172hclN4tDUuuWvFhAT8M88JKmcvJbaN8kWRTAAiky5CM6A',  phone_number_id='103290435735343')
resposne = messenger.send_reply_button(
        recipient_id="966555862924",
        button={
            "type": "button",
            "body": {
                "text": "This is a test button"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "This is button 1"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "this is button 2"
                        }
                    }
                ]
            }
      },
    )
print(resposne);
