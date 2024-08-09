USE `sesip-app`;

INSERT INTO User(username, password)
VALUES ('user1', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user2', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user3', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user4', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a');

INSERT INTO SecurityTarget (st_name, st_details, is_evaluated, is_valid, model, owner_id)
VALUES ('111', '{"TOE_NAME": "123", "SESIP_Level": 1}', True, TRUE, 'gpt-4o', 1),
       ('222', '{"TOE_NAME": "234", "SESIP_Level": 2}', True, FALSE, 'gpt-4o-mini', 4),
       ('333', NULL, FALSE, NULL, '', 2),
       ('444', '{"TOE_NAME": "456", "SESIP_Level": 4}', True, FALSE, 'gpt-4o-mini', 1),
       ('555', NULL, FALSE, NULL, '', 1),
       ('666', '{"TOE_NAME": "678", "SESIP_Level": 4}', True, FALSE, 'gpt-4o', 3),
       ('777', NULL, FALSE, NULL, '', 4),
       ('888', '{"TOE_NAME": "890", "SESIP_Level": 3}', True, TRUE, 'gpt-4o-mini', 2),
       ('999', NULl, FALSE, NULL, '', 3),
       ('000', '{"TOE_NAME": "012", "SESIP_Level": 3}', True, FALSE, 'gp-4o', 3);