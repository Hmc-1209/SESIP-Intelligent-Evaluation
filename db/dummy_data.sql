USE
`sesip-app`;

INSERT INTO User(username, password)
VALUES ('user1', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user2', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user3', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user4', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a');

INSERT INTO SecurityTarget (st_name, st_details, st_file, eval_details, eval_file, is_valid, owner_id)
VALUES ('111', '{"TOE": "123", "SESIP_Level": 1}', '1111', '1111', '1111', TRUE, 1),
       ('222', '{"TOE": "234", "SESIP_Level": 2}', '2222', '2222', '2222', FALSE, 4),
       ('333', '{"TOE": "345", "SESIP_Level": 3}', '3333', '3333', '3333', FALSE, 2),
       ('444', '{"TOE": "456", "SESIP_Level": 4}', '4444', '4444', '4444', FALSE, 1),
       ('555', '{"TOE": "567", "SESIP_Level": 2}', '5555', '5555', '5555', TRUE, 1),
       ('666', '{"TOE": "678", "SESIP_Level": 4}', '6666', '6666', '6666', FALSE, 3),
       ('777', '{"TOE": "789", "SESIP_Level": 2}', '7777', '7777', '7777', TRUE, 4),
       ('888', '{"TOE": "890", "SESIP_Level": 3}', '8888', '8888', '8888', TRUE, 2),
       ('999', '{"TOE": "901", "SESIP_Level": 1}', '9999', '9999', '9999', FALSE, 3),
       ('000', '{"TOE": "012", "SESIP_Level": 3}', '0000', '0000', '0000', FALSE, 3);