USE `sesip-app`;

INSERT INTO User(username, password)
VALUES ('user1', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user2', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user3', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user4', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a');

INSERT INTO SecurityTarget (st_name, st_details, is_evaluated, is_valid, owner_id)
VALUES ('111', '{"TOE": "123", "SESIP_Level": 1}', True, TRUE, 1),
       ('222', '{"TOE": "234", "SESIP_Level": 2}', True, FALSE, 4),
       ('333', '{"TOE": "345", "SESIP_Level": 3}', FALSE, NULL, 2),
       ('444', '{"TOE": "456", "SESIP_Level": 4}', True, FALSE, 1),
       ('555', '{"TOE": "567", "SESIP_Level": 2}', FALSE, NULL, 1),
       ('666', '{"TOE": "678", "SESIP_Level": 4}', True, FALSE, 3),
       ('777', '{"TOE": "789", "SESIP_Level": 2}', FALSE, NULL, 4),
       ('888', '{"TOE": "890", "SESIP_Level": 3}', True, TRUE, 2),
       ('999', '{"TOE": "901", "SESIP_Level": 1}', FALSE, NULL, 3),
       ('000', '{"TOE": "012", "SESIP_Level": 3}', True, FALSE, 3);