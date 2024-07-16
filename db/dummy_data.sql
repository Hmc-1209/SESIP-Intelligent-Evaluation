USE
`sesip-app`;

INSERT INTO User(username, password)
VALUES ('user1', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user2', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user3', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a'),
       ('user4', '$2b$12$OhOTSBsRHkf9TOqHzfCScODkj0bbsWBMfa97BqLHufvRYlv9W4W9a');

INSERT INTO SecurityTarget (st_name, create_date, update_date, sesip_level, is_valid, owner_id)
VALUES ('111', '2022-09-11', '2022-09-12', 1, TRUE, 1),
       ('222', '2022-09-15', '2022-09-23', 2, FALSE, 4),
       ('333', '2022-10-01', '2022-10-09', 3, FALSE, 2),
       ('444', '2022-10-05', '2022-10-06', 4, FALSE, 1),
       ('555', '2022-11-12', '2022-11-14', 2, TRUE, 1),
       ('666', '2022-11-15', '2022-11-21', 4, FALSE, 3),
       ('777', '2022-12-12', '2022-12-20', 2, TRUE, 4),
       ('888', '2023-01-01', '2023-01-03', 3, TRUE, 2),
       ('999', '2023-02-01', '2023-02-05', 1, FALSE, 3),
       ('000', '2023-02-10', '2023-02-16', 3, FALSE, 3);