import nexmo

client = nexmo.Client(key='fe9c0087', secret='b91e5377e5a92cc6')
#client = nexmo.Client(application_id='41a5b22e-99b8-4fdb-8ca5-9cd32e740499', private_key='fe9c0087')

response = client.send_message({'from': '12013505982', 'to': '2038028314', 'text': 'Hello world'})

response = response['messages'][0]

if response['status'] == '0':
  print('Sent message', response['message-id'])

  print('Remaining balance is', response['remaining-balance'])
else:
  print('Error:', response['error-text'])
