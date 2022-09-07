-- Keep a log of any SQL queries you execute as you solve the mystery.

-- To find the description of crime commited
SELECT description FROM crime_scene_reports
WHERE year = 2021
AND street = 'Humphrey Street'
AND month = 7;

-- To view the transcirpt and gather information about the crime
SELECT transcript, name FROM interviews WHERE year = 2021 AND month = 7 AND day = 28;

--ruth said 10mins after robbery the thief left in a car
SELECT id, license_plate, activity, minute  FROM bakery_security_logs WHERE year = 2021 AND hour = 10 AND month = 7 and minute >= 15 AND minute <= 25 AND day = 28;

--match license plate that entered with exiting one
SELECT id, license_plate, activity, minute  FROM bakery_security_logs WHERE year = 2021 AND hour = 9 AND month = 7  AND day = 28;

-- eugene saw thief withdrawing money from atm
SELECT id, account_number, amount, transaction_type FROM atm_transactions
WHERE atm_location = 'Leggett Street'
AND month = 7
AND day = 28
AND year = 2021;

-- list all calls less than 60s -> raymond transcript
SELECT id, caller, receiver, duration
FROM phone_calls
WHERE duration <= 60
AND month = 7
AND day = 28
AND year = 2021;

-- to find earliest flight on the 29th as per raymonds transcripts
SELECT origin_airport_id, destination_airport_id, hour, minute
FROM flights
WHERE month = 7
AND day = 29
AND year = 2021
ORDER BY hour ASC;

--find airport names with id of 4 and 8 as earliest flights origin airport was 8 and destination was 4
SELECT * FROM airports WHERE id = 4 OR id = 8;

-- going back to roots and listing all account numbers that withdrew money from atm on legett street on the day of the robbery.
SELECT account_number, amount
  FROM atm_transactions
  WHERE year = 2021
    AND month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw';

--get names and corresponding amount of people who withdrew money on day of crime as per eugenes statment
SELECT people.name, atm_transactions.amount
FROM people
JOIN bank_accounts
    ON bank_accounts.person_id = people.id
JOIN atm_transactions
    ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2021
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location = 'Leggett Street'
    AND atm_transactions.transaction_type = 'withdraw';

-- find the flight id of la guardia -> 36
SELECT flights.id, full_name, city, flights.hour, flights.minute
  FROM airports
  JOIN flights
    ON airports.id = flights.destination_airport_id
 WHERE flights.origin_airport_id =
       (SELECT id
          FROM airports
         WHERE city = 'Fiftyville')
   AND flights.year = 2021
   AND flights.month = 7
   AND flights.day = 29
 ORDER BY flights.hour, flights.minute;

-- list of passengers on flight to new york city -> Bruce and kenny showing up again
 SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat
  FROM people
  JOIN passengers
    ON people.passport_number = passengers.passport_number
  JOIN flights
    ON passengers.flight_id = flights.id
 WHERE flights.id = 36
 ORDER BY passengers.passport_number;

-- list of names of calleres where call is less than 60 -> Bruce again?
 SELECT name, phone_calls.duration
  FROM people
  JOIN phone_calls
    ON people.phone_number = phone_calls.caller
 WHERE phone_calls.year = 2021
   AND phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60
 ORDER BY phone_calls.duration;

 -- list of names who recieved a call -> all names could have helped edit: Robins call durarion is same as bruce
 SELECT name, phone_calls.duration
  FROM people
  JOIN phone_calls
    ON people.phone_number = phone_calls.receiver
 WHERE phone_calls.year = 2021
   AND phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60
   ORDER BY phone_calls.duration;

-- match the names of car owners with license plates that left within 10 mins of the theft as per ruths statment - bruce again?
   SELECT name, bakery_security_logs.hour, bakery_security_logs.minute
  FROM people
  JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
 WHERE bakery_security_logs.year = 2021
   AND bakery_security_logs.month = 7
   AND bakery_security_logs.day = 28
   AND bakery_security_logs.activity = 'exit'
   AND bakery_security_logs.hour = 10
   AND bakery_security_logs.minute >= 15
   AND bakery_security_logs.minute <= 25
 ORDER BY bakery_security_logs.minute;