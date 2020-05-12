echo 'Resetting Database'
echo ''
curl -X POST $1/api/v1/reset

echo 'Test 1: Get Users list (empty)'
echo ''
curl -X GET $1/api/v1/users

echo 'Test 2: Create New Users'
echo ''
curl -d '{"username":"zero"}' -H "Content-Type: application/json" -X POST $1/api/v1/users
curl -X GET $1/api/v1/users

echo 'Test 3: Delete specific user'
echo ''
curl -X DELETE $1/api/v1/users/1
curl -X GET $1/api/v1/users/1

echo 'Test 4: Create New Scores'
echo ''
curl -d '{"username":"zero"}' -H "Content-Type: application/json" -X POST $1/api/v1/users
curl -d '{"game_name": "mastermind", "value": 10.0}' -H "Content-Type: application/json" -X POST $1/api/v1/scores/2
curl -d '{"game_name": "connect_4", "value": 30.0}' -H "Content-Type: application/json" -X POST $1/api/v1/scores/2

echo 'Test 5: Get Scores'
echo ''
curl -X GET $1/api/v1/scores/2

