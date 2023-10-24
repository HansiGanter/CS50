-- Keep a log of any SQL queries you execute as you solve the mystery.

-- get first clue from crime scene report
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
--+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
--| id  | year | month | day |     street      |                                                                                                       description                                                                                                        |
--+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
--| 295 | 2021 | 7     | 28  | Humphrey Street | Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
--| 297 | 2021 | 7     | 28  | Humphrey Street | Littering took place at 16:36. No known witnesses.                                                                                                                                                                       |
--+-----+------+-------+-----+-----------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

-- get interviews of suspects
SELECT * FROM interviews WHERE year = 2021 AND month = 07 AND day = 28 AND transcript LIKE '%bakery%';
--+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
--| id  |  name   | year | month | day |                                                                                                                                                     transcript                                                                                                                                                      |
--+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
--| 161 | Ruth    | 2021 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
--| 162 | Eugene  | 2021 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
--| 163 | Raymond | 2021 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
--+-----+---------+------+-------+-----+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

-- get all license plate numbers that left the parking lot between 10:15 and 10:25
SELECT * FROM bakery_security_logs JOIN people ON bakery_security_logs.license_plate = people.license_plate WHERE year = 2021 AND month = 07 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;
--+-----+------+-------+-----+------+--------+----------+---------------+--------+---------+----------------+-----------------+---------------+
--| id  | year | month | day | hour | minute | activity | license_plate |   id   |  name   |  phone_number  | passport_number | license_plate |
--+-----+------+-------+-----+------+--------+----------+---------------+--------+---------+----------------+-----------------+---------------+
--| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       | 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
--| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
--| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       | 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
--| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
--| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       | 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
--| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
--| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
--| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
--+-----+------+-------+-----+------+--------+----------+---------------+--------+---------+----------------+-----------------+---------------+

-- get first flight next day out of city
SELECT * FROM flights JOIN airports ON flights.destination_airport_id = airports.id WHERE year = 2021 AND month = 07 AND day = 29 ORDER BY hour, minute;
--+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-------------------------------------+---------------+
--| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute | id | abbreviation |              full_name              |     city      |
--+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-------------------------------------+---------------+
--| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     | 4  | LGA          | LaGuardia Airport                   | New York City |
--| 43 | 8                 | 1                      | 2021 | 7     | 29  | 9    | 30     | 1  | ORD          | O'Hare International Airport        | Chicago       |
--| 23 | 8                 | 11                     | 2021 | 7     | 29  | 12   | 15     | 11 | SFO          | San Francisco International Airport | San Francisco |
--| 53 | 8                 | 9                      | 2021 | 7     | 29  | 15   | 20     | 9  | HND          | Tokyo International Airport         | Tokyo         |
--| 18 | 8                 | 6                      | 2021 | 7     | 29  | 16   | 0      | 6  | BOS          | Logan International Airport         | Boston        |
--+----+-------------------+------------------------+------+-------+-----+------+--------+----+--------------+-------------------------------------+---------------+

-- get all passengers on the flight to New York City where passport_number matches the people who left the parking lot after the theft
SELECT * FROM passengers WHERE flight_id in (SELECT flights.id FROM flights JOIN airports ON flights.destination_airport_id = airports.id WHERE year = 2021 AND month = 07 AND day = 29 ORDER BY hour, minute) AND passport_number in (SELECT people.passport_number FROM bakery_security_logs JOIN people ON bakery_security_logs.license_plate = people.license_pl
ate WHERE year = 2021 AND month = 07 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25);
--+-----------+-----------------+------+
--| flight_id | passport_number | seat |
--+-----------+-----------------+------+
--| 18        | 3592750733      | 4C   |
--| 36        | 1695452385      | 3B   |
--| 36        | 5773159633      | 4A   |
--| 36        | 8294398571      | 6C   |
--| 36        | 8496433585      | 7B   |
--+-----------+-----------------+------+

-- get all phone calls on July 28th 2021 where duration less than 1 minute
SELECT * FROM phone_calls WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60;
--+-----+----------------+----------------+------+-------+-----+----------+
--| id  |     caller     |    receiver    | year | month | day | duration |
--+-----+----------------+----------------+------+-------+-----+----------+
--| 221 | (130) 555-0289 | (996) 555-8899 | 2021 | 7     | 28  | 51       |
--| 224 | (499) 555-9472 | (892) 555-8872 | 2021 | 7     | 28  | 36       |
--| 233 | (367) 555-5533 | (375) 555-8161 | 2021 | 7     | 28  | 45       |
--| 251 | (499) 555-9472 | (717) 555-1342 | 2021 | 7     | 28  | 50       |
--| 254 | (286) 555-6063 | (676) 555-6554 | 2021 | 7     | 28  | 43       |
--| 255 | (770) 555-1861 | (725) 555-3243 | 2021 | 7     | 28  | 49       |
--| 261 | (031) 555-6622 | (910) 555-3251 | 2021 | 7     | 28  | 38       |
--| 279 | (826) 555-1652 | (066) 555-9701 | 2021 | 7     | 28  | 55       |
--| 281 | (338) 555-6650 | (704) 555-2131 | 2021 | 7     | 28  | 54       |
--+-----+----------------+----------------+------+-------+-----+----------+

-- get theft -> Bruce
SELECT pc.id AS pc_id, pc.caller AS pc_caller, pc.receiver AS pc_receiver, p.name AS p_name, p.phone_number AS p_phone, p.passport_number AS p_passport, p.license_plate AS p_license_plate FROM phone_calls pc
JOIN people p ON pc.caller = p.phone_number
JOIN bakery_security_logs b ON b.license_plate = p.license_plate
JOIN passengers pa ON pa.passport_number = p.passport_number
JOIN flights f ON pa.flight_id = f.id
JOIN bank_accounts ba ON p.id = ba.person_id
WHERE b.year = 2021
AND b.month = 07
AND b.day = 28
AND b.hour = 10
AND b.minute >= 15
AND b.minute <= 25
AND pc.year = 2021
AND pc.month = 7
AND pc.day = 28
AND pc.duration < 60
AND f.id = 36;
--+-------+----------------+----------------+--------+----------------+------------+-----------------+
--| pc_id |   pc_caller    |  pc_receiver   | p_name |    p_phone     | p_passport | p_license_plate |
--+-------+----------------+----------------+--------+----------------+------------+-----------------+
--| 233   | (367) 555-5533 | (375) 555-8161 | Bruce  | (367) 555-5533 | 5773159633 | 94KL13X         |
--+-------+----------------+----------------+--------+----------------+------------+-----------------+

-- get accomplice -> Bruce called Robin after being at the bakery
SELECT * FROM people WHERE phone_number in (SELECT phone_calls.receiver FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60 AND people.name = 'Bruce');
--+--------+-------+----------------+-----------------+---------------+
--|   id   | name  |  phone_number  | passport_number | license_plate |
--+--------+-------+----------------+-----------------+---------------+
--| 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
--+--------+-------+----------------+-----------------+---------------+