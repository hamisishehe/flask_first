-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 27, 2025 at 03:10 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fyp`
--

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `id` int(11) NOT NULL,
  `course_code` varchar(100) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `semester` int(11) NOT NULL,
  `is_tutorial` tinyint(1) NOT NULL,
  `is_lecture` tinyint(1) NOT NULL,
  `time_difference` int(11) NOT NULL,
  `coordinator_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`id`, `course_code`, `course_name`, `semester`, `is_tutorial`, `is_lecture`, `time_difference`, `coordinator_id`) VALUES
(1, 'LG 102', 'Communication Skills', 1, 1, 1, 3, 1),
(2, 'CP 111', 'Principles of Programming Languages', 1, 1, 1, 3, 1),
(3, 'DS 102', 'Development Perspectives', 1, 1, 1, 3, 1),
(4, 'IT 111', 'Introduction to Information Technology', 1, 1, 1, 3, 1),
(5, 'TN 112', 'Linear Algebra for ICT', 1, 1, 1, 3, 1),
(6, 'TN 111', 'Discrete Mathematics for ICT', 1, 1, 1, 3, 1),
(7, 'IA 112', 'Mathematical Foundations of Information Security', 1, 1, 1, 3, 1),
(8, 'TN 113', 'Calculus', 1, 1, 1, 3, 1),
(16, 'IA 417', 'Cyber Threat Intelligence', 1, 1, 1, 3, 1),
(17, 'CG 221', 'Fundamentals of IoT', 1, 1, 1, 3, 1),
(18, 'CT 411', 'Embedded Systems I', 1, 1, 1, 3, 1),
(19, 'CT 412', 'Parallel Computing', 1, 1, 1, 3, 1),
(20, 'TN 412', 'Digital Signal Processing', 1, 1, 1, 3, 1),
(21, 'CG 411', 'Computer Engineering Project I', 1, 1, 1, 3, 1),
(22, 'CT 413', 'Operating Systems Internals', 1, 1, 1, 3, 1),
(23, 'IA 314', 'Biometric Security', 1, 1, 1, 3, 1),
(24, 'CS 431', 'Software Engineering Project I', 1, 1, 1, 3, 1),
(25, 'CT 312', 'Computer Maintenance', 1, 1, 1, 3, 1),
(26, 'IM 411', 'Human-Computer Interaction', 1, 1, 1, 3, 1),
(27, 'CP 412', 'Programming', 1, 1, 1, 3, 1),
(28, 'CS 411', 'Software Reverse Engineering', 1, 1, 1, 3, 1),
(29, 'BT 312', 'Electronic and Mobile Commerce', 1, 1, 1, 3, 1),
(30, 'CD 312', 'Multimedia Content Development', 1, 1, 1, 3, 1),
(31, 'CP 314', 'Distributed Computing', 1, 1, 1, 3, 1),
(32, 'TN 411', 'Mobile Communication', 1, 1, 1, 3, 1),
(33, 'TN 413', 'Information Theory and Coding', 1, 1, 1, 3, 1),
(34, 'TN 431', 'Telecommunications Engineering Project I', 1, 1, 1, 3, 1),
(35, 'IA 311', 'Network Forensics', 1, 1, 1, 3, 1),
(36, 'CD 431', 'Content Engineering Project I', 1, 1, 1, 3, 1),
(37, 'CD 411', 'Project Studio Production and Sound Synthesis', 1, 1, 1, 3, 1),
(38, 'CD 412', 'Video and Audio Systems II', 1, 1, 1, 3, 1),
(39, 'IM 411', 'Human Computer Interaction', 1, 1, 1, 3, 1),
(40, 'SI 312', 'Organizational Management', 1, 1, 1, 3, 1),
(41, 'LW 4110', 'Legal Aspects in Cyber Security', 1, 1, 1, 3, 1),
(42, 'IA 418', 'Cyber Criminology and Techniques', 1, 1, 1, 3, 1),
(43, 'CS 418', 'Cyber Security and Digital Forensics Engineering Project I', 1, 1, 1, 3, 1),
(44, 'LW 4110', 'Legal Aspects in Cyber Security Hardware Forensics', 1, 1, 1, 3, 1),
(47, 'AF 111', 'Introduction to Financial Accounting', 1, 1, 1, 3, 1),
(48, 'MG 111', 'Principles of Business', 1, 1, 1, 3, 1),
(54, 'CD 112', 'Foundations of Instructional Design', 1, 1, 1, 3, 1),
(63, 'CD 111', 'Digital Media Psychology', 1, 1, 1, 3, 1),
(72, 'EC 111', 'Fundamentals of Electrical Engineering', 1, 1, 1, 3, 1),
(78, 'CD 113', 'Fundamentals of Content Engineering', 1, 1, 1, 3, 1),
(79, 'CN 111', 'Fundamentals to Telecommunications Enginnering', 1, 1, 1, 3, 1),
(80, 'CD 111', 'Digital Media Psychology', 1, 1, 1, 3, 1),
(81, 'EME 314', 'ICT Entrepreneurship', 1, 1, 1, 3, 3),
(82, 'S1 311', 'Professional Ethics', 1, 1, 1, 3, 3),
(83, 'BT 413', 'ICT Project Management', 1, 1, 1, 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `course_matrix`
--

CREATE TABLE `course_matrix` (
  `id` int(11) NOT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_matrix`
--

INSERT INTO `course_matrix` (`id`, `instructor_id`, `course_id`, `student_id`) VALUES
(5, 19, 1, 5),
(6, 19, 1, 1),
(7, 19, 1, 9),
(8, 19, 1, 41),
(9, 19, 1, 23),
(10, 19, 1, 20),
(11, 19, 1, 12),
(12, 19, 1, 22),
(13, 19, 1, 16),
(14, 1, 2, 41),
(15, 1, 2, 23),
(16, 1, 2, 5),
(17, 1, 2, 1),
(18, 1, 2, 22),
(19, 1, 2, 16),
(20, 1, 2, 12),
(21, 16, 3, 1),
(22, 16, 3, 9),
(23, 16, 3, 5),
(24, 16, 3, 23),
(25, 16, 3, 12),
(26, 16, 3, 22),
(27, 16, 3, 16),
(28, 16, 3, 20),
(29, 18, 4, 1),
(30, 18, 4, 9),
(31, 18, 4, 5),
(32, 18, 4, 22),
(33, 18, 4, 16),
(34, 18, 4, 23),
(35, 18, 4, 20),
(36, 18, 4, 38),
(37, 18, 4, 41),
(38, 18, 4, 12),
(39, 15, 5, 1),
(40, 15, 5, 5),
(41, 15, 5, 9),
(42, 15, 5, 12),
(43, 14, 6, 1),
(44, 14, 6, 5),
(45, 14, 6, 41),
(46, 14, 6, 38),
(47, 14, 6, 9),
(48, 14, 6, 20),
(49, 15, 7, 1),
(50, 15, 7, 12),
(51, 15, 7, 19),
(52, 15, 7, 9),
(53, 4, 8, 1),
(54, 4, 8, 9),
(55, 2, 47, 20),
(56, 4, 48, 20),
(57, 17, 63, 16),
(58, 17, 63, 22),
(59, 17, 63, 24),
(60, 17, 80, 16),
(61, 17, 80, 22),
(62, 17, 80, 24),
(63, 7, 79, 23),
(64, 7, 79, 5),
(65, 8, 72, 5),
(66, 8, 72, 23),
(67, 16, 78, 22),
(68, 16, 78, 16),
(69, 16, 78, 24),
(70, 5, 54, 16),
(71, 5, 54, 22),
(72, 5, 54, 24),
(73, 4, 8, 12),
(74, 98, 16, 27),
(75, 98, 16, 15),
(76, 11, 81, 15),
(77, 11, 81, 8),
(78, 11, 81, 34),
(79, 11, 81, 27),
(80, 104, 28, 4),
(81, 83, 34, 34),
(82, 83, 21, 8),
(83, 77, 23, 27),
(84, 82, 83, 4),
(85, 82, 83, 8),
(86, 82, 83, 34),
(87, 82, 83, 29),
(88, 82, 83, 18),
(89, 82, 83, 31),
(90, 82, 83, 37),
(91, 82, 83, 40),
(92, 82, 83, 43),
(93, 82, 83, 11),
(94, 82, 82, 4),
(95, 82, 82, 8),
(96, 82, 82, 34),
(97, 82, 82, 29),
(98, 82, 82, 18),
(99, 82, 82, 31),
(100, 82, 82, 37),
(101, 82, 82, 40),
(102, 82, 82, 15),
(103, 82, 82, 27),
(104, 82, 26, 4),
(105, 82, 26, 29),
(106, 82, 26, 38),
(107, 85, 24, 11),
(108, 85, 29, 4);

-- --------------------------------------------------------

--
-- Stand-in structure for view `course_matrix_view`
-- (See below for the actual view)
--
CREATE TABLE `course_matrix_view` (
`course_matrix_id` int(11)
,`course_id` int(11)
,`course_name` varchar(100)
,`course_code` varchar(100)
,`semester` int(11)
,`instructor_id` int(11)
,`instructor_first_name` varchar(100)
,`instructor_last_name` varchar(100)
,`instructor_email` varchar(120)
,`instructor_title` varchar(120)
,`student_id` int(11)
,`programme` varchar(100)
,`total_students` varchar(10)
);

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `title` varchar(120) NOT NULL,
  `coordinator_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`id`, `first_name`, `middle_name`, `last_name`, `phone_number`, `email`, `title`, `coordinator_id`) VALUES
(1, 'Isaac', 'Mahenge', 'Isaac', '711121211', 'Isaac@udom.co.tz', 'Mr.', 1),
(2, 'Julius', 'Webbo', 'Julius', '711121212', 'Julius@udom.co.tz', 'Mr.', 1),
(3, 'Baraka', 'Jungwa', 'baraka', '711121213', 'baraka@udom.co.tz', 'Mr.', 1),
(4, 'Rukia', 'Mwifunyi', 'mwifunyi', '711121214', 'Rukia@udom.co.tz', 'Dr.', 1),
(5, 'Mariam', 'Said', 'said', '711121215', 'mariam@udom.co.tz', 'Ms.', 1),
(6, 'Hamis', 'Fereji', 'hamis', '711121216', 'hamisi@udom.co.tz', 'Mr.', 1),
(7, 'Carina', 'Carina', 'carina', '711121217', 'carina@udom.co.tz', 'Dr.', 1),
(8, 'Wilbard', 'Masue', 'masue', '711121218', 'wilbard@udom.co.tz', 'Mr.', 1),
(9, 'Simba', 'Mwinyimbara', 'Mwinyimbara', '711121219', 'simba@udom.co.tz', 'Mr.', 1),
(10, 'Shingwa', 'Magashi', 'Magashi', '711121220', 'shingwa@udom.co.tz', 'Dr.', 1),
(11, 'Emmanuel', 'Mambali', 'Mambali', '711121221', 'emmanuel@udom.co.tz', 'Mr.', 1),
(12, 'Glory', 'Lema', 'Lema', '711121222', 'glory@udom.co.tz', 'Ms.', 1),
(13, 'Wivina', 'Muyungi', 'Muyungi', '711121223', 'wivina@udom.co.tz', 'Ms.', 1),
(14, 'Samson', 'Nyondo', 'Nyondo', '711121224', 'samson@udom.co.tz', 'Mr.', 1),
(15, 'Nasolwa', 'Edson', 'Edson', '711121225', 'nasolwa@udom.co.tz', 'Mr.', 1),
(16, 'Lucian', 'Ngeze', 'Ngeze', '711121226', 'lucian@udom.co.tz', 'Dr.', 1),
(17, 'Mevis', 'Steven', 'Steven', '711121227', 'mevis@udom.co.tz', 'Ms.', 1),
(18, 'Gilbert', 'Gilbert', 'Gilbert', '711121228', 'gilbert@udom.co.tz', 'Dr.', 1),
(19, 'Andwele', 'Mwakasege', 'Mwakasege', '0700000000', 'Andwele@udom.co.tz', 'Dr', 1),
(20, 'Emmanuel', NULL, NULL, NULL, 'Emmanuel@udom.to.tz', 'Mr', 1),
(77, 'Mustafa', NULL, 'Mohsin', NULL, 'mustafamohsin@udom.to.tz', 'Dr', 1),
(78, 'Florence', NULL, 'Rashid', NULL, 'florencerashid1@udom.to.tz', 'Dr', 1),
(79, 'Rukia', NULL, 'Mwifunyi', NULL, 'rukiamwifunyi@udom.to.tz', 'Dr', 1),
(80, 'Florence', NULL, 'Rashid', NULL, 'florencerashid@udom.to.tz', 'Dr', 1),
(81, 'Jabhera', NULL, 'Matogoro', NULL, 'jabheramatogoro@udom.to.tz', 'Dr', 1),
(82, 'Majuto', NULL, 'Manyilizu', NULL, 'majutomanyilizu@udom.to.tz', 'Dr', 1),
(83, 'Goodiel', NULL, 'Moshi', NULL, 'goodielmoshi@udom.to.tz', 'Dr', 1),
(84, 'Yona', NULL, 'Zakaria', NULL, 'yonazakaria@udom.to.tz', 'Mr', 1),
(85, 'Nixon', NULL, 'Mtonyole', NULL, 'nixonmtonyole@udom.to.tz', 'Mr', 1),
(86, 'Anthony', NULL, 'Mwombeki', NULL, 'anthonymwombeki@udom.to.tz', 'Mr', 1),
(87, 'Lucian', NULL, 'Ngeze', NULL, 'lucianngeze@udom.to.tz', 'Dr', 1),
(88, 'Abraham', NULL, 'Macha', NULL, 'abrahammacha@udom.to.tz', 'Mr', 1),
(89, 'Chande', NULL, 'Kasita', NULL, 'chandekasita@udom.to.tz', 'Mr', 1),
(90, 'Ramadhani', NULL, 'Mbaga', NULL, 'ramadhanimbaga@udom.to.tz', 'Mr', 1),
(91, 'Siphael', NULL, 'Betuel', NULL, 'siphaelbetuel@udom.to.tz', 'Mr', 1),
(92, 'Nima', NULL, 'Shidende', NULL, 'nimashidende@udom.to.tz', 'Dr', 1),
(93, 'Aliko', NULL, 'Matola', NULL, 'alikomatola@udom.to.tz', 'Mr', 1),
(94, 'Bernard', NULL, 'Julius', NULL, 'bernardjulius@udom.to.tz', 'Mr', 1),
(95, 'Naufal', NULL, 'Kitonka', NULL, 'naufalkitonka@udom.to.tz', 'Mr', 1),
(96, 'Everyjustus', NULL, 'Barongo', NULL, 'everyjustusbarongo@udom.to.tz', 'Mr', 1),
(97, 'Christina', NULL, 'Murro', NULL, 'christinamurro@udom.to.tz', 'Dr', 1),
(98, 'Daniel', NULL, 'Ngondya', NULL, 'danielngondya@udom.to.tz', 'Dr', 1),
(99, 'Amani', NULL, 'David', NULL, 'amanidavid@udom.to.tz', 'Dr', 1),
(100, 'Jairos', NULL, 'Shinzeh', NULL, 'jairosshinzeh@udom.to.tz', 'Dr', 1),
(101, 'Godfrey', NULL, 'Molela', NULL, 'godfreymolela@udom.to.tz', 'Mr', 1),
(102, 'Deo', NULL, 'Shao', NULL, 'deoshao@udom.to.tz', 'Dr', 1),
(103, 'Emanuel', NULL, 'Malya', NULL, 'emanuelmalya@udom.to.tz', 'Mr', 1),
(104, 'Leyla', 'leyla', 'layla', '0777676767', 'leyla@udom.co.tz', 'Mrs', 3);

-- --------------------------------------------------------

--
-- Table structure for table `instructor_course`
--

CREATE TABLE `instructor_course` (
  `id` int(11) NOT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `priority` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `scheduled_class`
--

CREATE TABLE `scheduled_class` (
  `id` int(11) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `day` varchar(20) NOT NULL,
  `time_slot` varchar(20) NOT NULL,
  `venue` varchar(100) NOT NULL,
  `student_groups` varchar(200) NOT NULL,
  `instructor` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `programme` varchar(100) NOT NULL,
  `total_students` varchar(10) NOT NULL,
  `coordinator_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `programme`, `total_students`, `coordinator_id`) VALUES
(1, 'SE1', '70', 1),
(2, 'SE2', '80', 1),
(3, 'SE3', '81', 1),
(4, 'SE4', '82', 1),
(5, 'CE1', '83', 1),
(6, 'CE2', '84', 1),
(7, 'CE3', '85', 1),
(8, 'CE4', '86', 1),
(9, 'CS1', '87', 1),
(10, 'CS2', '88', 1),
(11, 'CS3', '89', 1),
(12, 'CNISE1', '60', 1),
(13, 'CNISE2', '55', 1),
(14, 'CNISE3', '60', 1),
(15, 'CNISE4', '61', 1),
(16, 'IDIT 1', '70', 1),
(17, 'IDIT2', '80', 1),
(18, 'IDIT3', '70', 1),
(19, 'CSDFE1', '72', 1),
(20, 'BIS1', '80', 1),
(21, 'IDIT1', '88', 1),
(22, 'MTA1', '96', 1),
(23, 'TE1', '104', 1),
(24, 'DCBE1', '112', 1),
(25, 'CSDFE2', '73', 1),
(26, 'CSDFE3', '74', 1),
(27, 'CSDFE4', '74', 1),
(28, 'BIS2', '81', 1),
(29, 'BIS3', '82', 1),
(30, 'MTA2', '97', 1),
(31, 'MTA3', '98', 1),
(32, 'TE2', '105', 1),
(33, 'TE3', '106', 1),
(34, 'TE4', '107', 1),
(35, 'DCBE2', '113', 1),
(36, 'DCBE3', '114', 1),
(37, 'DCBE4', '115', 1),
(38, 'IS1', '116', 1),
(39, 'IS2', '117', 1),
(40, 'IS3', '118', 1),
(41, 'HIS1', '119', 1),
(42, 'HIS2', '120', 1),
(43, 'HIS3', '121', 1),
(44, 'IST1', '30', 1),
(45, 'IST2', '40', 1);

-- --------------------------------------------------------

--
-- Table structure for table `student_course`
--

CREATE TABLE `student_course` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) NOT NULL,
  `phone_number` varchar(10) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('COORDINATOR','ADMIN','TIMETABLEMASTER') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `middle_name`, `last_name`, `phone_number`, `email`, `password_hash`, `role`) VALUES
(1, 'coordinator', 'A.', 'Doe', '0744982380', 'coordinator@example.com', 'scrypt:32768:8:1$IkpcRkBQCJtvkMlo$f77807d22f9912b533903d77c90b0463ec36cf1a5dc72ed81fa51c9dae7db3645f6c4898f5e6edc202a795b9fb1dc1df9c51c460f8412637198fb8354c228a4a', 'TIMETABLEMASTER'),
(2, 'timetablemaster', 'B.', 'timetablemaster', '0744982310', 'timetablemaster@udom.co.tz', 'scrypt:32768:8:1$Hbq6mGq0KIWjnysy$6d3acf93da2b885252126c578e019842bdeaa2c41c6e3762f77da81dd313ef757c5717296abb9e2d127900a6dead93cf37d1ea5a8bd00da0d34fb1c1972d0c35', 'TIMETABLEMASTER'),
(3, 'coordinator', 'A.', 'coordinator', '1234567890', 'coordinator@udom.co.tz', 'scrypt:32768:8:1$deiqXXx9lPYONxpE$fbe1eb46c031409f4ddf376d57eae4d7a5c6a9c3b8610fe1da0fc430fc611155156ddac964d67ee9f040f0eee8fbfe4b1431436ccc653cdf0ab8cc4b57b181f4', 'COORDINATOR'),
(4, 'admin', NULL, 'admin', '0987654321', 'admin@udom.co.tz', 'scrypt:32768:8:1$SWcKfm32I3j8pdKj$9409e3b2d6e0a7d37be01020a499686321dea8bedc343bb1af7bfa0959686f3b627ca21fb493d33b7df4210ae977016505cb3cd7afd5afc82b2e29aa04ac94a3', 'ADMIN');

-- --------------------------------------------------------

--
-- Table structure for table `venue`
--

CREATE TABLE `venue` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `exam_capacity` int(11) NOT NULL,
  `teaching_capacity` int(11) NOT NULL,
  `type` enum('LAB','CLASS') NOT NULL,
  `coordinator_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `venue`
--

INSERT INTO `venue` (`id`, `name`, `location`, `exam_capacity`, `teaching_capacity`, `type`, `coordinator_id`) VALUES
(1, 'LRB 105', 'CIVE', 216, 312, 'CLASS', 1),
(2, 'LRB 106', 'CIVE', 216, 312, 'CLASS', 1),
(3, 'LRB 101', 'CIVE', 108, 108, 'CLASS', 1),
(4, 'LRB 102', 'CIVE', 108, 108, 'CLASS', 1),
(5, 'LRB 103', 'CIVE', 108, 108, 'CLASS', 1),
(6, 'LRB 104', 'CIVE', 108, 108, 'CLASS', 1),
(7, 'LRB 004C', 'CIVE', 108, 108, 'CLASS', 1),
(8, 'LRB 005B', 'CIVE', 108, 108, 'CLASS', 1),
(9, 'LRB 003D', 'CIVE', 108, 108, 'CLASS', 1),
(10, 'MULT_LAB', 'CIVE', 80, 80, 'CLASS', 1),
(11, 'SE_LAB', 'CIVE', 70, 70, 'CLASS', 1),
(12, 'GENERAL_LAB', 'CIVE', 70, 70, 'CLASS', 1),
(13, 'LRA 020', 'CIVE', 100, 108, 'CLASS', 1),
(14, ' LRA 103', 'CIVE', 100, 108, 'CLASS', 1),
(15, 'LRA 104', 'CIVE', 100, 108, 'CLASS', 1),
(16, 'FL 1', 'CIVE', 150, 312, 'CLASS', 1),
(17, 'FL 2', 'CIVE', 150, 312, 'CLASS', 1),
(18, 'LRA 018', 'CIVE', 70, 108, 'CLASS', 1),
(19, 'ELE_LAB', 'CIVE', 70, 108, 'CLASS', 1),
(20, 'LRA 019', 'CIVE', 70, 108, 'CLASS', 1),
(21, 'LRB 004D', 'CIVE', 70, 108, 'CLASS', 1),
(22, 'LRA 008', 'CIVE', 70, 108, 'CLASS', 1),
(23, 'LRA 021', 'CIVE', 70, 108, 'CLASS', 1),
(24, 'CIVE-AUDITORIUM', 'CIVE', 1375, 1375, 'CLASS', 1);

-- --------------------------------------------------------

--
-- Structure for view `course_matrix_view`
--
DROP TABLE IF EXISTS `course_matrix_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `course_matrix_view`  AS SELECT `cm`.`id` AS `course_matrix_id`, `c`.`id` AS `course_id`, `c`.`course_name` AS `course_name`, `c`.`course_code` AS `course_code`, `c`.`semester` AS `semester`, `i`.`id` AS `instructor_id`, `i`.`first_name` AS `instructor_first_name`, `i`.`last_name` AS `instructor_last_name`, `i`.`email` AS `instructor_email`, `i`.`title` AS `instructor_title`, `s`.`id` AS `student_id`, `s`.`programme` AS `programme`, `s`.`total_students` AS `total_students` FROM (((`course_matrix` `cm` join `course` `c` on(`cm`.`course_id` = `c`.`id`)) join `instructor` `i` on(`cm`.`instructor_id` = `i`.`id`)) join `students` `s` on(`cm`.`student_id` = `s`.`id`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coordinator_id` (`coordinator_id`);

--
-- Indexes for table `course_matrix`
--
ALTER TABLE `course_matrix`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructor_id` (`instructor_id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `coordinator_id` (`coordinator_id`);

--
-- Indexes for table `instructor_course`
--
ALTER TABLE `instructor_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructor_id` (`instructor_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `scheduled_class`
--
ALTER TABLE `scheduled_class`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coordinator_id` (`coordinator_id`);

--
-- Indexes for table `student_course`
--
ALTER TABLE `student_course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `course_id` (`course_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `venue`
--
ALTER TABLE `venue`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coordinator_id` (`coordinator_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT for table `course_matrix`
--
ALTER TABLE `course_matrix`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=109;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=105;

--
-- AUTO_INCREMENT for table `instructor_course`
--
ALTER TABLE `instructor_course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `scheduled_class`
--
ALTER TABLE `scheduled_class`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=166;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `student_course`
--
ALTER TABLE `student_course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `venue`
--
ALTER TABLE `venue`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `course_matrix`
--
ALTER TABLE `course_matrix`
  ADD CONSTRAINT `course_matrix_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`id`),
  ADD CONSTRAINT `course_matrix_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  ADD CONSTRAINT `course_matrix_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

--
-- Constraints for table `instructor`
--
ALTER TABLE `instructor`
  ADD CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `instructor_course`
--
ALTER TABLE `instructor_course`
  ADD CONSTRAINT `instructor_course_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`id`),
  ADD CONSTRAINT `instructor_course_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `student_course`
--
ALTER TABLE `student_course`
  ADD CONSTRAINT `student_course_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `student_course_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`);

--
-- Constraints for table `venue`
--
ALTER TABLE `venue`
  ADD CONSTRAINT `venue_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
