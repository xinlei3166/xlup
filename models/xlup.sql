/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : localhost:3306
 Source Schema         : xlup

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 24/12/2018 11:03:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for access_key
-- ----------------------------
DROP TABLE IF EXISTS `access_key`;
CREATE TABLE `access_key` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标志',
  `user_id` int(11) NOT NULL,
  `access_key_id` varchar(64) NOT NULL COMMENT 'access_key_id',
  `access_key_secret` varchar(64) NOT NULL COMMENT 'access_key_secret',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_secret_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='访问秘钥';

-- ----------------------------
-- Records of access_key
-- ----------------------------
BEGIN;
INSERT INTO `access_key` VALUES (1, 0, 1, 'XLU3SjKgueJWHqtSyr', '51b0c82c5ef9f7e464fa4a1dbc1a21c2', '2018-11-23 10:58:25', '2018-12-23 23:01:38');
INSERT INTO `access_key` VALUES (2, 0, 3, 'XL9ghW758s8TWVmXY4', '86e911fbd76082ff2342af003a14d69f', '2018-11-26 17:33:32', '2018-12-23 23:01:42');
INSERT INTO `access_key` VALUES (4, 0, 2, 'XLNnpEQDGcdcujUWgL', '653ca7e4128224bbf1292767360345ab', '2018-12-17 02:30:14', '2018-12-23 23:01:45');
INSERT INTO `access_key` VALUES (6, 0, 14, 'XLBUSqJjHcje3PyD5V', '12a62a70c3a4ee91678613dc3814f88d', '2018-12-24 10:10:55', '2018-12-24 10:10:55');
COMMIT;

-- ----------------------------
-- Table structure for migratehistory
-- ----------------------------
DROP TABLE IF EXISTS `migratehistory`;
CREATE TABLE `migratehistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `migrated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of migratehistory
-- ----------------------------
BEGIN;
INSERT INTO `migratehistory` VALUES (4, '001_auto', '2018-11-16 16:35:29');
INSERT INTO `migratehistory` VALUES (7, '002_auto', '2018-11-23 10:29:40');
COMMIT;

-- ----------------------------
-- Table structure for pic
-- ----------------------------
DROP TABLE IF EXISTS `pic`;
CREATE TABLE `pic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标志',
  `title` varchar(32) DEFAULT NULL COMMENT '标题',
  `description` varchar(64) DEFAULT NULL COMMENT '描述',
  `path` varchar(128) NOT NULL COMMENT '图片路径',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `pic_user_id_index` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8 COMMENT='图片';

-- ----------------------------
-- Records of pic
-- ----------------------------
BEGIN;
INSERT INTO `pic` VALUES (31, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (32, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (33, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (34, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (35, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (37, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (38, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (46, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (47, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (48, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (49, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (50, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (51, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (52, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (53, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (55, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (56, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (57, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (58, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (59, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (60, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (61, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (62, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 1, '2018-11-26 14:19:53', '2018-11-26 14:20:33');
INSERT INTO `pic` VALUES (63, 0, '标题', '描述', 'pic/2018/11/26/jv3BF6Yt8Jpx.jpeg', 8, '2018-11-26 14:19:53', '2018-12-19 21:43:45');
INSERT INTO `pic` VALUES (64, 0, '李白', '王者荣耀-李白', 'pic/2018/12/23/bBqeScusZDvx.jpeg', 1, '2018-12-23 17:01:50', '2018-12-23 17:01:50');
INSERT INTO `pic` VALUES (67, 0, '李白', '王者李白', 'pic/2018/12/23/AbYVshVGRSgF.jpeg', 1, '2018-12-23 19:21:09', '2018-12-23 19:21:09');
INSERT INTO `pic` VALUES (70, 0, '测试上传', '测试上传', 'pic/2018/12/24/U8x4Xq8Ehnx4.jpeg', 1, '2018-12-24 10:57:26', '2018-12-24 10:57:26');
COMMIT;

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标志',
  `name` varchar(32) NOT NULL COMMENT '角色名称',
  `codename` varchar(32) NOT NULL COMMENT 'codename',
  `description` varchar(64) DEFAULT NULL COMMENT '描述',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_codename_uindex` (`codename`),
  UNIQUE KEY `role_name_uindex` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='角色表';

-- ----------------------------
-- Records of role
-- ----------------------------
BEGIN;
INSERT INTO `role` VALUES (1, 0, '管理员', 'admin', '管理员', '2018-11-14 14:39:18', '2018-11-14 14:39:18');
INSERT INTO `role` VALUES (2, 0, '普通用户', 'user', '普通用户', '2018-11-14 14:39:18', '2018-11-14 14:39:18');
COMMIT;

-- ----------------------------
-- Table structure for setting
-- ----------------------------
DROP TABLE IF EXISTS `setting`;
CREATE TABLE `setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标志',
  `name` varchar(64) NOT NULL COMMENT '项目名',
  `codename` varchar(64) NOT NULL COMMENT 'codename',
  `value` varchar(64) NOT NULL COMMENT '项目值',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='系统设置';

-- ----------------------------
-- Records of setting
-- ----------------------------
BEGIN;
INSERT INTO `setting` VALUES (1, 0, '用户认证-key', 'auth_key', 'GU97WLcXkHWAUBemMWNTTU', '2018-11-14 16:34:56', '2018-11-14 16:34:56');
COMMIT;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) DEFAULT '0' COMMENT '删除标志',
  `username` varchar(64) NOT NULL COMMENT '用户名',
  `password` varchar(128) NOT NULL COMMENT '用户密码',
  `nickname` varchar(32) NOT NULL COMMENT '昵称',
  `head_img` varchar(128) DEFAULT NULL,
  `gender` varchar(12) NOT NULL DEFAULT 'female' COMMENT '性别',
  `email` varchar(64) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(11) DEFAULT NULL COMMENT '电话',
  `role_id` int(11) NOT NULL COMMENT '角色',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email_uindex` (`email`),
  UNIQUE KEY `user_phone_uindex` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COMMENT='用户表';

-- ----------------------------
-- Records of user
-- ----------------------------
BEGIN;
INSERT INTO `user` VALUES (1, 0, 'admin', '425afdc44dee6ef5b4620586316783e7895a3a883fbf3b2a7fb1bcb65b23be4c', '管理员', 'pic/2018/12/24/AYUNRqv75nJV.jpeg', 'male', 'admin@qq.com', '16666666666', 1, '2018-11-14 15:10:29', '2018-12-24 10:56:50');
INSERT INTO `user` VALUES (2, 0, 'user', 'c42309bc7e844542385ac20b83edbb00465ff46b9c19154edb9026b9e4add894', '普通用户', NULL, 'female', 'user@qq.com', '16666666661', 2, '2018-11-14 15:13:29', '2018-12-19 21:39:52');
INSERT INTO `user` VALUES (3, 0, 'junxi', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi@qq.com', '16666666662', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (4, 0, 'junxi1', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi1@qq.com', '16666666663', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (5, 0, 'junxi2', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi2@qq.com', '16666666664', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (6, 0, 'junxi3', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi3@qq.com', '16666666665', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (9, 0, 'junxi4', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi4@qq.com', '16666666656', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (10, 0, 'junxi5', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi5@qq.com', '16666666667', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (11, 0, 'junxi6', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi6@qq.com', '16666666668', 2, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user` VALUES (12, 0, 'junxi7', '8a789976a7ed6826e39e7e47cc49e8112f92837781a7376283c5231af9755a15', '君惜', NULL, 'male', 'junxi7123123123123123123123123123123213123123123213@qq.com', '16666666669', 2, '2018-11-26 17:33:32', '2018-12-19 00:53:44');
INSERT INTO `user` VALUES (14, 0, 'junxi9', '64f864459af50b61a518310f90897996d3e4de2c4a7f98b5fb48acc0095c5520', '君惜', NULL, 'male', 'junxi9@qq.com', '16666666659', 2, '2018-12-24 10:10:55', '2018-12-24 10:10:55');
COMMIT;

-- ----------------------------
-- Table structure for user_secret
-- ----------------------------
DROP TABLE IF EXISTS `user_secret`;
CREATE TABLE `user_secret` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标志',
  `secret` varchar(64) NOT NULL COMMENT '用户秘钥',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `user_secret_user_id_index` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='用户秘钥';

-- ----------------------------
-- Records of user_secret
-- ----------------------------
BEGIN;
INSERT INTO `user_secret` VALUES (1, 0, 'f97c5d29941bfb1b2fdab0874906ab82', 1, '2018-11-14 15:19:01', '2018-11-14 15:19:01');
INSERT INTO `user_secret` VALUES (2, 0, 'b8a9f715dbb64fd5c56e7783c6820a61', 2, '2018-11-14 15:19:01', '2018-11-14 15:19:01');
INSERT INTO `user_secret` VALUES (3, 0, 'd0a067f78a2dabf839e0d858b585095d', 3, '2018-11-26 17:33:32', '2018-11-26 17:33:32');
INSERT INTO `user_secret` VALUES (5, 0, 'f2b9b9efa300d3b3ef68654f40bb71a7', 14, '2018-12-24 10:10:55', '2018-12-24 10:10:55');
COMMIT;

-- ----------------------------
-- Table structure for video
-- ----------------------------
DROP TABLE IF EXISTS `video`;
CREATE TABLE `video` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `delete_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除标志',
  `title` varchar(32) DEFAULT NULL COMMENT '标题',
  `description` varchar(64) DEFAULT NULL COMMENT '描述',
  `pic` varchar(128) NOT NULL COMMENT '预览图',
  `path` varchar(128) NOT NULL COMMENT '视频路径',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `video_user_id_index` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8 COMMENT='视频';

-- ----------------------------
-- Records of video
-- ----------------------------
BEGIN;
INSERT INTO `video` VALUES (4, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (5, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (6, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (7, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (9, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (10, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (11, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (12, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (13, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (14, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (15, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (16, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (17, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (18, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (19, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (20, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (21, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (22, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (23, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (24, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (25, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (26, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (27, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (28, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 8, '2018-11-26 15:00:30', '2018-12-19 22:43:04');
INSERT INTO `video` VALUES (30, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (31, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (32, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (33, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (34, 0, '标题', '描述', 'pic/2018/11/26/rXvnahd3q2bb.jpeg', 'video/2018/11/26/ziziUsDzrD7F.mp4', 1, '2018-11-26 15:00:30', '2018-12-18 10:18:58');
INSERT INTO `video` VALUES (35, 0, '梦工场视频', '梦工场视频', 'pic/2018/12/23/fMzYZcWn3Zxe.png', 'video/2018/12/23/7gQAafhWESFK.mp4', 1, '2018-12-23 19:09:18', '2018-12-23 19:09:18');
INSERT INTO `video` VALUES (36, 0, '公益星视频', '公益星视频', 'pic/2018/12/23/owxBJ7JNeUsj.jpeg', 'video/2018/12/23/Wgon7wNteQTS.mp4', 1, '2018-12-23 19:18:11', '2018-12-23 19:18:11');
INSERT INTO `video` VALUES (38, 0, '李白视频', '李白视频', 'pic/2018/12/23/s8h3BddeZwnf.jpeg', 'video/2018/12/23/a2q4narAtq46.mp4', 1, '2018-12-23 19:21:39', '2018-12-23 19:21:39');
INSERT INTO `video` VALUES (39, 0, '测试视频上传', '测试视频上传', 'pic/2018/12/23/yMNBer2USHKj.jpeg', 'video/2018/12/23/v8PEQqKSbojc.mp4', 1, '2018-12-23 19:22:52', '2018-12-23 19:22:52');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
