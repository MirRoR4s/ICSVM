delete from fba.sys_fuzz_test_fields;
delete from fba.sys_fuzz_test_cases;
delete from fba.sys_fuzz_test_suites;

INSERT INTO fba.sys_fuzz_test_suites(
    id, name, description, is_system, created_time, updated_time) VALUES (1, 'system', '系统保留测试套件', 1, NOW(), null
);

INSERT INTO fba.sys_fuzz_test_cases(
    id, name, description, suite_id, created_time, updated_time) VALUES (1, 'ftp1', '系统保留测试用例1', 1, NOW(), null
);

INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    1, 'user1', '{"type": "String", "name": "key", "default_value": "USER"}', NOW(), null
);
INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    1, 'user2', '{"type": "Delim", "name": "space", "default_value": " "}', NOW(), null
);
INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    1, 'user3', '{"type": "String", "name": "val", "default_value": "anonymous"}', NOW(), null
);
INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    1, 'user4', '{"type": "Static", "name": "end", "default_value": "\\r\\n"}', NOW(), null
);

INSERT INTO fba.sys_fuzz_test_cases(
    id, name, description, suite_id, created_time, updated_time) VALUES (2, 'ftp2', '系统保留测试用例2', 1, NOW(), null
);

INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    2, 'passw1', '{"type": "String", "name": "key", "default_value": "PASS"}', NOW(), null
);
INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    2, 'passw2', '{"type": "Delim", "name": "space", "default_value": " "}', NOW(), null
);
INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    2, 'passw3', '{"type": "String", "name": "val", "default_value": "james"}', NOW(), null
);
INSERT INTO fba.sys_fuzz_test_fields (case_id, name, attribute, created_time, updated_time) VALUES (
    2, 'passw4', '{"type": "Static", "name": "end", "default_value": "\\r\\n"}', NOW(), null
);
