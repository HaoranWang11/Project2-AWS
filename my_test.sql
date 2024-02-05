/*
 Navicat Premium Data Transfer

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50741
 Source Host           : 192.168.1.9:3306
 Source Schema         : my_test

 Target Server Type    : MySQL
 Target Server Version : 50741
 File Encoding         : 65001

 Date: 04/02/2024 21:37:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for table_users
-- ----------------------------
DROP TABLE IF EXISTS `table_users`;
CREATE TABLE `table_users`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '',
  `password` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '',
  `firstname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '',
  `lastname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '',
  `register_time` datetime(0) NULL DEFAULT NULL,
  `last_login_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of table_users
-- ----------------------------
INSERT INTO `table_users` VALUES (2, 'aaa', '123', 'John', 'Smith', 'aasda@asdasdasd.com', '2023-10-27 04:29:20', '2024-02-04 21:36:07');
INSERT INTO `table_users` VALUES (3, 'bbb', '123', 'Sarah', 'Johnson', 'sadasd@cddes.com', '2023-11-01 15:27:03', '2023-11-01 15:27:07');
INSERT INTO `table_users` VALUES (4, 'ccc', '123', 'Michael', 'Brown', 'cadaes@ecddeq.com', '2024-02-04 19:44:38', '2024-02-04 19:44:47');
INSERT INTO `table_users` VALUES (6, 'ddd', '123', 'aaa', 'bbb', 'asdasd@dasdaa', '2024-02-04 21:32:48', NULL);

SET FOREIGN_KEY_CHECKS = 1;
