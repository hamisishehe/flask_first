-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 16, 2025 at 11:51 AM
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
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('776909fd29d0');

-- --------------------------------------------------------

--
-- Table structure for table `collage`
--

CREATE TABLE `collage` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `short_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `collage`
--

INSERT INTO `collage` (`id`, `name`, `short_name`, `description`) VALUES
(1, 'College of Informatics and Virtual Education', 'CIVE', 'CIVE'),
(2, 'College of Education ', 'CoED', 'CoED');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `id` int(11) NOT NULL,
  `course_name` varchar(100) NOT NULL,
  `course_code` varchar(100) NOT NULL,
  `semester` int(11) NOT NULL,
  `is_tutorial` tinyint(1) NOT NULL,
  `is_lecture` tinyint(1) NOT NULL,
  `is_practical` tinyint(1) NOT NULL,
  `coordinator_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`id`, `course_name`, `course_code`, `semester`, `is_tutorial`, `is_lecture`, `is_practical`, `coordinator_id`, `department_id`) VALUES
(87, 'Communication Skills', 'LG 102', 1, 1, 1, 0, 2, 3),
(88, 'Development Perspectives', 'DS 102', 1, 1, 1, 0, 2, 3),
(89, 'Calculus', 'TN 113', 1, 1, 1, 0, 2, 5),
(90, 'Principles of Programming Languages', 'CP 111', 1, 1, 1, 0, 2, 5),
(91, 'Discrete Mathematics for ICT', 'TN 111', 1, 1, 1, 0, 2, 5),
(92, 'Introduction to Information Technology', 'IT 111', 1, 1, 1, 0, 2, 5),
(93, 'Mathematical Foundations of Info Security', 'IA 112', 1, 1, 1, 0, 2, 5),
(94, 'Linear Algebra for ICT', 'TN 112', 1, 1, 1, 0, 2, 5),
(95, 'Object Oriented Programming in Java', 'cp 215', 1, 1, 1, 0, 2, 5),
(96, 'Data Structures and Algorithms Analysis', 'CP 213', 1, 1, 1, 0, 2, 5),
(97, 'Information Security Technologies', 'IA 211', 1, 1, 1, 0, 2, 5),
(98, 'Computer Networking Protocols', 'CN 211', 1, 1, 1, 1, 2, 5),
(99, 'Computer Organization and Architecture I', 'CT 211', 1, 1, 1, 0, 2, 5),
(100, 'Systems Analysis and Design', 'CP 212', 1, 1, 1, 0, 2, 5),
(101, 'Introduction To Linux/Unix Systems', 'CP 211', 1, 1, 1, 1, 2, 5),
(102, 'Measurements and Instrumentation Engineering', 'EC 212', 1, 1, 1, 0, 2, 5),
(103, 'Calculus for Engineers', 'TN 211', 1, 1, 1, 0, 2, 5),
(104, 'Analogue Electronics', 'CT 212', 1, 1, 1, 1, 2, 5),
(105, 'Computer Forensics and Investigation', 'IA 212', 1, 1, 1, 0, 2, 5),
(106, 'ICT Entrepreneurship', 'EME 314', 1, 1, 1, 0, 2, 5),
(107, 'Professional Ethics and Conduct', 'SI 311', 1, 1, 1, 0, 2, 5),
(108, 'Database Security', 'IA 414', 1, 1, 1, 0, 2, 5),
(109, 'ICT Project Management', 'BT 413', 1, 1, 1, 0, 2, 5),
(110, 'Computer Networks and Information Security', 'CS 419', 1, 1, 1, 0, 2, 5),
(111, 'Cloud Computing Security', 'IA 416', 1, 1, 1, 0, 2, 5),
(112, 'Wireless Networks and Mobile Computing', 'CN 411', 1, 1, 1, 0, 2, 5),
(113, 'Information Security Management and Standards', 'IA 415', 1, 1, 1, 0, 2, 5),
(114, 'Cyber Threat Intelligence', 'IA 417', 1, 1, 1, 0, 2, 5),
(115, 'Fundamentals of IoT', 'CG 221', 1, 1, 1, 0, 2, 5),
(116, 'Embedded Systems I', 'CT 411', 1, 1, 1, 1, 2, 5),
(117, 'Parallel Computing', 'CT 412', 1, 1, 1, 0, 2, 5),
(118, 'Digital Signal Processing', 'TN 412', 1, 1, 1, 0, 2, 5),
(119, 'Computer Engineering Project I', 'CG 411', 1, 1, 1, 0, 2, 5),
(120, 'Operating Systems Internals', 'CT 413', 1, 1, 1, 0, 2, 5),
(121, 'Biometric Security', 'IA 314', 1, 1, 1, 0, 2, 5),
(122, 'Software Engineering Project I', 'CS 431', 1, 1, 1, 0, 2, 5),
(123, 'Computer Maintenance', 'CT 312', 1, 1, 1, 0, 2, 5),
(124, 'Human-Computer Interaction', 'IM 411', 1, 1, 1, 0, 2, 5),
(125, 'C# Programming', 'CP 412', 1, 1, 1, 0, 2, 5),
(126, 'Software Reverse Engineering', 'CS 411', 1, 1, 1, 0, 2, 5),
(127, 'Electronic and Mobile Commerce', 'BT 312', 1, 1, 1, 0, 2, 5),
(128, 'Multimedia Content Development', 'CD 312', 1, 1, 1, 0, 2, 5),
(129, 'Distributed Computing', 'CP 314', 1, 1, 1, 0, 2, 5),
(130, 'Mobile Communication', 'TN 411', 1, 1, 1, 0, 2, 5),
(131, 'Information Theory and Coding', 'TN 413', 1, 1, 1, 0, 2, 5),
(132, 'Telecommunications Engineering Project I', 'TN 431', 1, 1, 1, 0, 2, 5),
(133, 'Network Forensics', 'IA 311', 1, 1, 1, 0, 2, 5),
(134, 'Content Engineering Project I', 'CD 431', 1, 1, 1, 0, 2, 5),
(135, 'Project Studio Production and Sound Synthesis', 'CD 411', 1, 1, 1, 0, 2, 5),
(136, 'Video and Audio Systems II', 'CD 412', 1, 1, 1, 0, 2, 5),
(137, 'Legal Aspects in Cyber Security', 'LW 4110', 1, 1, 1, 0, 2, 5),
(138, 'Cyber Security and Digital Forensics Engineering Project I', 'CS 418', 1, 1, 1, 0, 2, 5);

-- --------------------------------------------------------

--
-- Table structure for table `course_matrix`
--

CREATE TABLE `course_matrix` (
  `id` int(11) NOT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `program_group` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_matrix`
--

INSERT INTO `course_matrix` (`id`, `instructor_id`, `course_id`, `student_id`, `program_group`) VALUES
(124, 105, 89, 27, ''),
(125, 105, 89, 31, ''),
(126, 105, 89, 38, ''),
(127, 105, 89, 42, ''),
(128, 1, 90, 15, 'A'),
(129, 1, 90, 21, 'A'),
(130, 1, 90, 24, 'A'),
(131, 106, 90, 27, 'B'),
(132, 106, 90, 31, 'B'),
(133, 106, 90, 34, 'B'),
(134, 106, 90, 38, 'B'),
(135, 106, 90, 46, 'B'),
(136, 105, 91, 27, 'A'),
(137, 105, 91, 31, 'A'),
(138, 105, 91, 34, 'A'),
(139, 105, 91, 38, 'A'),
(140, 105, 91, 42, 'A'),
(141, 1, 92, 27, 'A'),
(142, 1, 92, 34, 'A'),
(143, 1, 92, 38, 'A'),
(144, 1, 92, 42, 'A'),
(145, 1, 92, 31, 'A'),
(146, 15, 93, 27, ''),
(147, 15, 93, 31, ''),
(148, 15, 93, 38, ''),
(149, 105, 94, 27, ''),
(150, 105, 94, 34, ''),
(151, 105, 94, 38, ''),
(152, 105, 94, 42, ''),
(153, 105, 94, 31, ''),
(154, 19, 87, 15, ''),
(155, 19, 87, 21, ''),
(156, 19, 87, 24, ''),
(157, 19, 87, 27, ''),
(158, 19, 87, 31, ''),
(159, 19, 87, 34, ''),
(160, 19, 87, 38, ''),
(161, 19, 87, 42, ''),
(162, 19, 87, 46, ''),
(163, 16, 88, 15, ''),
(164, 16, 88, 21, ''),
(165, 16, 88, 24, ''),
(166, 16, 88, 27, ''),
(167, 16, 88, 31, ''),
(168, 16, 88, 34, ''),
(169, 16, 88, 38, ''),
(170, 16, 88, 42, ''),
(171, 16, 88, 46, ''),
(172, 107, 95, 16, 'A'),
(173, 107, 95, 22, 'A'),
(174, 107, 95, 25, 'A'),
(175, 107, 95, 46, 'A'),
(176, 96, 95, 32, 'B'),
(177, 96, 95, 35, 'B'),
(178, 96, 95, 28, 'B'),
(179, 96, 95, 39, 'B'),
(180, 96, 95, 43, 'B'),
(181, 1, 96, 28, ''),
(182, 1, 96, 32, ''),
(183, 1, 96, 35, ''),
(184, 98, 98, 28, ''),
(185, 98, 98, 32, ''),
(186, 98, 98, 35, ''),
(187, 98, 98, 39, ''),
(188, 98, 98, 43, ''),
(189, 110, 101, 28, 'A'),
(190, 110, 101, 32, 'A'),
(191, 110, 101, 43, 'A'),
(192, 110, 101, 47, 'A'),
(193, 110, 101, 39, 'A'),
(194, 4, 106, 37, 'A'),
(195, 4, 106, 41, 'A'),
(196, 4, 106, 45, 'A'),
(197, 6, 107, 17, ''),
(198, 6, 107, 26, ''),
(199, 6, 107, 30, ''),
(200, 6, 107, 37, ''),
(201, 6, 107, 41, ''),
(202, 6, 107, 45, ''),
(203, 6, 107, 33, ''),
(204, 6, 107, 23, ''),
(205, 98, 108, 41, ''),
(206, 98, 108, 45, ''),
(207, 98, 110, 41, ''),
(208, 82, 109, 17, ''),
(209, 82, 109, 23, ''),
(210, 82, 109, 30, ''),
(211, 82, 109, 33, ''),
(212, 82, 109, 45, ''),
(213, 82, 109, 48, ''),
(214, 82, 109, 41, ''),
(215, 3, 112, 41, ''),
(216, 98, 114, 41, ''),
(217, 98, 114, 45, ''),
(218, 15, 115, 37, ''),
(219, 4, 116, 37, ''),
(220, 15, 117, 37, ''),
(221, 77, 120, 37, ''),
(222, 77, 121, 37, ''),
(223, 84, 124, 30, ''),
(224, 84, 124, 41, ''),
(225, 84, 124, 33, ''),
(226, 84, 124, 45, ''),
(227, 84, 124, 17, ''),
(228, 102, 125, 30, ''),
(229, 103, 127, 30, ''),
(230, 103, 127, 33, ''),
(231, 103, 127, 41, ''),
(232, 93, 129, 30, ''),
(233, 93, 129, 33, ''),
(234, 93, 129, 41, ''),
(235, 105, 131, 37, ''),
(236, 99, 138, 45, ''),
(237, 99, 137, 45, ''),
(238, 99, 121, 45, '');

-- --------------------------------------------------------

--
-- Stand-in structure for view `course_matrix_view`
-- (See below for the actual view)
--
CREATE TABLE `course_matrix_view` (
`course_matrix_id` int(11)
,`program_group` varchar(100)
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
,`programme_code` varchar(100)
,`total_students` varchar(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `short_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `collage_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`id`, `name`, `short_name`, `description`, `collage_id`) VALUES
(3, 'Information Systems and Technology', 'IST', 'IST', 1),
(4, 'Electronics and Telecommunications Engineering', 'ETE', 'ETE', 1),
(5, 'Computer Science and Engineering', 'CSE', 'CSE', 1);

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `id` int(11) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `gender` varchar(120) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `title` varchar(120) NOT NULL,
  `coordinator_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`id`, `first_name`, `middle_name`, `last_name`, `gender`, `phone_number`, `email`, `title`, `coordinator_id`, `department_id`) VALUES
(1, 'Isaac', 'Mahenge', 'Isaac', 'MALE', '711121211', 'Isaac@udom.co.tz', 'Mr.', 5, 5),
(2, 'Julius', 'Webbo', 'Julius', 'MALE', '711121212', 'Julius@udom.co.tz', 'Mr.', 5, 5),
(3, 'Baraka', 'Jungwa', 'baraka', 'MALE', '711121213', 'baraka@udom.co.tz', 'Mr.', 5, 5),
(4, 'Rukia', 'Mwifunyi', 'mwifunyi', 'FEMALE', '711121214', 'Rukia@udom.co.tz', 'Dr.', 5, 5),
(5, 'Mariam', 'Said', 'said', 'FEMALE', '711121215', 'mariam@udom.co.tz', 'Ms.', 5, 5),
(6, 'Hamis', 'Fereji', 'hamis', 'MALE', '711121216', 'hamisi@udom.co.tz', 'Mr.', 5, 5),
(7, 'Carina', 'Carina', 'carina', 'FEMALE', '711121217', 'carina@udom.co.tz', 'Dr.', 5, 5),
(8, 'Wilbard', 'Masue', 'masue', 'MALE', '711121218', 'wilbard@udom.co.tz', 'Mr.', 5, 5),
(9, 'Simba', 'Mwinyimbara', 'Mwinyimbara', 'MALE', '711121219', 'simba@udom.co.tz', 'Mr.', 5, 5),
(10, 'Shingwa', 'Magashi', 'Magashi', 'MALE', '711121220', 'shingwa@udom.co.tz', 'Dr.', 5, 5),
(11, 'Emmanuel', 'Mambali', 'Mambali', 'MALE', '711121221', 'emmanuel@udom.co.tz', 'Mr.', 5, 5),
(12, 'Glory', 'Lema', 'Lema', 'FEMALE', '711121222', 'glory@udom.co.tz', 'Ms.', 5, 5),
(13, 'Wivina', 'Muyungi', 'Muyungi', 'FEMALE', '711121223', 'wivina@udom.co.tz', 'Ms.', 4, 3),
(14, 'Samson', 'Nyondo', 'Nyondo', 'MALE', '711121224', 'samson@udom.co.tz', 'Mr.', 5, 5),
(15, 'Nasolwa', 'Edson', 'Edson', 'MALE', '711121225', 'nasolwa@udom.co.tz', 'Mr.', 5, 5),
(16, 'Lucian', 'Ngeze', 'Ngeze', 'MALE', '711121226', 'lucian@udom.co.tz', 'Dr.', 4, 3),
(17, 'Mevis', 'Steven', 'Steven', 'FEMALE', '711121227', 'mevis@udom.co.tz', 'Ms.', 4, 3),
(18, 'Gilbert', 'Gilbert', 'Gilbert', 'MALE', '711121228', 'gilbert@udom.co.tz', 'Dr.', 4, 3),
(19, 'Andwele', 'Mwakasege', 'Mwakasege', 'MALE', '700000000', 'Andwele@udom.co.tz', 'Dr', 4, 3),
(20, 'Emmanuel', '', 'Emanuel', 'MALE', '700000001', 'Emmanuel@udom.to.tz', 'Mr', 4, 3),
(77, 'Mustafa', '', 'Mohsin', 'MALE', '700000002', 'mustafamohsin@udom.to.tz', 'Dr', 5, 5),
(78, 'Florence', '', 'Rashid', 'MALE', '700000003', 'florencerashid1@udom.to.tz', 'Dr', 5, 5),
(79, 'Rukia', '', 'Mwifunyi', 'FEMALE', '700000004', 'rukiamwifunyi@udom.to.tz', 'Dr', 4, 5),
(80, 'Florence', '', 'Rashid', 'MALE', '700000005', 'florencerashid@udom.to.tz', 'Dr', 5, 5),
(81, 'Jabhera', '', 'Matogoro', 'MALE', '700000006', 'jabheramatogoro@udom.to.tz', 'Dr', 5, 5),
(82, 'Majuto', '', 'Manyilizu', 'MALE', '700000007', 'majutomanyilizu@udom.to.tz', 'Dr', 5, 5),
(83, 'Goodiel', '', 'Moshi', 'MALE', '700000008', 'goodielmoshi@udom.to.tz', 'Dr', 5, 5),
(84, 'Yona', '', 'Zakaria', 'MALE', '700000009', 'yonazakaria@udom.to.tz', 'Mr', 4, 5),
(85, 'Nixon', '', 'Mtonyole', 'MALE', '700000010', 'nixonmtonyole@udom.to.tz', 'Mr', 5, 5),
(86, 'Anthony', '', 'Mwombeki', 'MALE', '700000011', 'anthonymwombeki@udom.to.tz', 'Mr', 4, 5),
(87, 'Lucian', '', 'Ngeze', 'MALE', '700000012', 'lucianngeze@udom.to.tz', 'Dr', 4, 3),
(88, 'Abraham', '', 'Macha', 'MALE', '700000013', 'abrahammacha@udom.to.tz', 'Mr', 5, 5),
(89, 'Chande', '', 'Kasita', 'MALE', '700000014', 'chandekasita@udom.to.tz', 'Mr', 4, 3),
(90, 'Ramadhani', '', 'Mbaga', 'MALE', '700000015', 'ramadhanimbaga@udom.to.tz', 'Mr', 5, 5),
(91, 'Siphael', '', 'Betuel', 'MALE', '700000016', 'siphaelbetuel@udom.to.tz', 'Mr', 5, 5),
(92, 'Nima', '', 'Shidende', 'MALE', '700000017', 'nimashidende@udom.to.tz', 'Dr', 4, 5),
(93, 'Aliko', '', 'Matola', 'MALE', '700000018', 'alikomatola@udom.to.tz', 'Mr', 4, 5),
(94, 'Bernard', '', 'Julius', 'MALE', '700000019', 'bernardjulius@udom.to.tz', 'Mr', 4, 5),
(95, 'Naufal', '', 'Kitonka', 'MALE', '700000020', 'naufalkitonka@udom.to.tz', 'Mr', 4, 5),
(96, 'Everyjustus', '', 'Barongo', 'MALE', '700000021', 'everyjustusbarongo@udom.to.tz', 'Mr', 4, 5),
(97, 'Christina', '', 'Murro', 'FEMALE', '700000022', 'christinamurro@udom.to.tz', 'Dr', 5, 3),
(98, 'Daniel', '', 'Ngondya', 'MALE', '700000023', 'danielngondya@udom.to.tz', 'Dr', 5, 5),
(99, 'Amani', '', 'David', 'MALE', '700000024', 'amanidavid@udom.to.tz', 'Dr', 5, 5),
(100, 'Jairos', '', 'Shinzeh', 'MALE', '700000025', 'jairosshinzeh@udom.to.tz', 'Dr', 5, 5),
(101, 'Godfrey', '', 'Molela', 'MALE', '700000026', 'godfreymolela@udom.to.tz', 'Mr', 5, 5),
(102, 'Deo', '', 'Shao', 'MALE', '700000027', 'deoshao@udom.to.tz', 'Dr', 5, 5),
(103, 'Emanuel', '', 'Malya', 'MALE', '700000028', 'emanuelmalya@udom.to.tz', 'Mr', 5, 5),
(104, 'Leyla', 'leyla', 'layla', 'FEMALE', '777676767', 'leyla@udom.co.tz', 'Mrs', 5, 5),
(105, 'Pascal', 'Charles', 'Charles', 'Male', '0711121212', 'pascalcharles@gmail.com', 'Mr', 2, 5),
(106, 'Leonard', 'Msele', 'Msele', 'Male', '0711232323', 'leonard@gmail.com', 'Prof', 2, 5),
(107, 'feruzi', 'hassan', 'hassan', 'Male', '0713112233', 'feruzihassan@gmail.com', 'Mr', 2, 5),
(108, 'Everijustus', 'Balo', 'Balo', 'Male', '0711121223', 'Everijustus@gmail.com', 'Mr', 2, 5),
(109, 'Bakii', 'seif', 'bakii', 'Male', '0712121212', 'bakii@gmail.com', 'Mr', 2, 5),
(110, 'justin', 'woiso', 'justin', 'Male', '0712112233', 'justin@gmail.com', 'Mr', 2, 5),
(111, 'Christina', 'Murro', 'Murro', 'Female', '0712332244', 'Christina@gmail.com', 'Dr', 2, 5);

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
  `programme_code` varchar(100) NOT NULL,
  `programme` varchar(100) NOT NULL,
  `total_students` varchar(11) DEFAULT NULL,
  `coordinator_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `programme_code`, `programme`, `total_students`, `coordinator_id`, `department_id`) VALUES
(15, 'Business Information System', 'BIS1', '78', 4, 3),
(16, 'Business Information System', 'BIS2', '62', 4, 3),
(17, 'Business Information System', 'BIS3', '69', 4, 3),
(21, 'Instructional Design and Information  Technology ', 'IDIT1', '50', 4, 3),
(22, 'Instructional Design and Information  Technology ', 'IDIT2', '90', 4, 3),
(23, 'Instructional Design and Information  Technology ', 'IDIT3', '95', 4, 3),
(24, 'Multimedia Technology and Animation', 'MTA1', '106', 4, 3),
(25, 'Multimedia Technology and Animation', 'MTA2', '90', 4, 3),
(26, 'Multimedia Technology and Animation', 'MTA3', '80', 4, 3),
(27, 'Software Engineering', 'SE1', '92', 5, 5),
(28, 'Software Engineering', 'SE2', '70', 5, 5),
(29, 'Software Engineering', 'SE3', '69', 5, 5),
(30, 'Software Engineering', 'SE4', '65', 5, 5),
(31, 'Computer Science', 'CS1', '88', 5, 5),
(32, 'Computer Science', 'CS2', '69', 5, 5),
(33, 'Computer Science', 'CS3', '40', 5, 5),
(34, 'Computer Engineering', 'CE1', '40', 5, 5),
(35, 'Computer Engineering', 'CE2', '59', 5, 5),
(36, 'Computer Engineering', 'CE3', '79', 5, 5),
(37, 'Computer Engineering', 'CE4', '89', 5, 5),
(38, 'Computer Networks and Information Security  Engineering', 'CNISE1', '59', 5, 5),
(39, 'Computer Networks and Information Security  Engineering', 'CNISE2', '50', 5, 5),
(40, 'Computer Networks and Information Security  Engineering', 'CNISE3', '99', 5, 5),
(41, 'Computer Networks and Information Security  Engineering', 'CNISE4', '88', 5, 5),
(42, 'Cyber Security and Digital Forensics  Engineering ', 'CSDFE1', '80', 5, 5),
(43, 'Cyber Security and Digital Forensics  Engineering ', 'CSDFE2', '60', 5, 5),
(44, 'Cyber Security and Digital Forensics  Engineering ', 'CSDFE3', '55', 5, 5),
(45, 'Cyber Security and Digital Forensics  Engineering ', 'CSDFE4', '55', 5, 5),
(46, 'Health Information System', 'HIS1', '77', 4, 3),
(47, 'Health Information System', 'HIS2', '77', 4, 3),
(48, 'Health Information System', 'HIS3', '66', 4, 3);

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
  `department` varchar(100) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('COORDINATOR','ADMIN','TIMETABLEMASTER') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `middle_name`, `last_name`, `phone_number`, `email`, `department`, `password_hash`, `role`) VALUES
(1, 'timetablemaster', 'B.', 'timetablemaster', '0744982310', 'timetablemaster@udom.co.tz', '', 'scrypt:32768:8:1$egKoVC3dKbmtQOTs$2cdfcaf9b2ba8dd428ba97111443b911bc8476e4d6b6ca50527c4a6a85707e3176db5c40a60b15640c0ca80f7cad9973e1897a7b8252a2da350d482933a6a7bd', 'TIMETABLEMASTER'),
(2, 'coordinator', 'A.', 'coordinator', '1234567890', 'coordinator@udom.co.tz', 'CSE', 'scrypt:32768:8:1$EGl4tNpQU70d2evf$e91f38fb3b2082edfcb6376872aa5c6b11b36c6dffd46ae84434f060eff727e011366f6ec19b2ffa1ccac5811ad364f11369bcf2f5ec3bdb974e7e006a865a8c', 'COORDINATOR'),
(3, 'admin', NULL, 'admin', '0987654321', 'admin@udom.co.tz', '', 'scrypt:32768:8:1$BTtyNjr65KDYgKk1$f585ac54d8d77d3c52b16e590968c99490be8f67ae41c12f15309b221b3799574a721689593b417c1d3be78577a796fd99f3f585eb3033d4795c026ffe991e96', 'ADMIN'),
(4, 'Hamisi', 'shafii', 'shehe', '0744982380', 'hamisishehe@gmail.com', 'IST', 'scrypt:32768:8:1$DNiSCjFS0Ttb4Nkj$f8ed7896f95c28c7e5a8df5a895804f458eaf12a4f258aea1bdaba3b31832fc68abfb0b6fabbb29655365d73f65d86e4fada5aa108e6da3a4fbbcfb9cef9b252', 'COORDINATOR'),
(5, 'hamisi', 'nuru', 'shehe', '0653918817', 'hamisinuru83@gmail.com', 'CSE', 'scrypt:32768:8:1$exwky7niNwXJilr8$d9dc1f8c1bb39854ad608d364e75dacdeb147cd50a3a6a9ad08993b15bed53fd82eac2ece96b2cb9f37114a31b452e792b1ba89feb1dbeed3a89aedabe32e2a1', 'COORDINATOR');

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
  `type` enum('LAB','CLASS') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `venue`
--

INSERT INTO `venue` (`id`, `name`, `location`, `exam_capacity`, `teaching_capacity`, `type`) VALUES
(1, 'LRB 105', 'CIVE', 108, 217, 'CLASS'),
(2, 'LRB 106', 'CIVE', 216, 216, 'CLASS'),
(3, 'LRB 101', 'CIVE', 55, 111, 'CLASS'),
(4, 'LRB 102', 'CIVE', 108, 108, 'CLASS'),
(5, 'LRB 103', 'CIVE', 108, 108, 'CLASS'),
(6, 'LRB 104', 'CIVE', 108, 108, 'CLASS'),
(7, 'LRB 004C', 'CIVE', 108, 108, 'CLASS'),
(8, 'LRB 005B', 'CIVE', 108, 108, 'CLASS'),
(9, 'LRB 003D', 'CIVE', 108, 108, 'CLASS'),
(10, 'MULT_LAB', 'CIVE', 50, 100, 'CLASS'),
(11, 'SE_LAB', 'CIVE', 70, 70, 'CLASS'),
(12, 'GENERAL_LAB', 'CIVE', 70, 70, 'CLASS'),
(13, 'LRA 020', 'CIVE', 100, 100, 'CLASS'),
(14, 'LRA 103', 'CIVE', 100, 100, 'CLASS'),
(15, 'LRA 104', 'CIVE', 100, 100, 'CLASS'),
(16, 'FL 1', 'CIVE', 150, 150, 'CLASS'),
(17, 'FL 2', 'CIVE', 185, 370, 'CLASS'),
(18, 'LRA 018', 'CIVE', 70, 70, 'CLASS'),
(19, 'ELE_LAB', 'CIVE', 70, 70, 'CLASS'),
(20, 'LRA 019', 'CIVE', 70, 70, 'CLASS'),
(21, 'LRB 004D', 'CIVE', 70, 70, 'CLASS'),
(22, 'LRA 008', 'CIVE', 70, 70, 'CLASS'),
(23, 'LRA 021', 'CIVE', 70, 70, 'CLASS'),
(24, 'Auditoriam', 'CIVE', 700, 1400, 'CLASS');

-- --------------------------------------------------------

--
-- Structure for view `course_matrix_view`
--
DROP TABLE IF EXISTS `course_matrix_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `course_matrix_view`  AS SELECT `cm`.`id` AS `course_matrix_id`, `cm`.`program_group` AS `program_group`, `c`.`id` AS `course_id`, `c`.`course_name` AS `course_name`, `c`.`course_code` AS `course_code`, `c`.`semester` AS `semester`, `i`.`id` AS `instructor_id`, `i`.`first_name` AS `instructor_first_name`, `i`.`last_name` AS `instructor_last_name`, `i`.`email` AS `instructor_email`, `i`.`title` AS `instructor_title`, `s`.`id` AS `student_id`, `s`.`programme` AS `programme`, `s`.`programme_code` AS `programme_code`, `s`.`total_students` AS `total_students` FROM (((`course_matrix` `cm` join `course` `c` on(`cm`.`course_id` = `c`.`id`)) join `instructor` `i` on(`cm`.`instructor_id` = `i`.`id`)) join `students` `s` on(`cm`.`student_id` = `s`.`id`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `collage`
--
ALTER TABLE `collage`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id`),
  ADD KEY `coordinator_id` (`coordinator_id`),
  ADD KEY `department_id` (`department_id`);

--
-- Indexes for table `course_matrix`
--
ALTER TABLE `course_matrix`
  ADD PRIMARY KEY (`id`),
  ADD KEY `instructor_id` (`instructor_id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`id`),
  ADD KEY `collage_id` (`collage_id`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `coordinator_id` (`coordinator_id`),
  ADD KEY `department_id` (`department_id`);

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
  ADD KEY `coordinator_id` (`coordinator_id`),
  ADD KEY `department_id` (`department_id`);

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
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `collage`
--
ALTER TABLE `collage`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=139;

--
-- AUTO_INCREMENT for table `course_matrix`
--
ALTER TABLE `course_matrix`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=239;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=112;

--
-- AUTO_INCREMENT for table `instructor_course`
--
ALTER TABLE `instructor_course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `scheduled_class`
--
ALTER TABLE `scheduled_class`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `student_course`
--
ALTER TABLE `student_course`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `course_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`);

--
-- Constraints for table `course_matrix`
--
ALTER TABLE `course_matrix`
  ADD CONSTRAINT `course_matrix_ibfk_1` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`id`),
  ADD CONSTRAINT `course_matrix_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  ADD CONSTRAINT `course_matrix_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

--
-- Constraints for table `department`
--
ALTER TABLE `department`
  ADD CONSTRAINT `department_ibfk_1` FOREIGN KEY (`collage_id`) REFERENCES `collage` (`id`);

--
-- Constraints for table `instructor`
--
ALTER TABLE `instructor`
  ADD CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `instructor_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`);

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
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`coordinator_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `students_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`);

--
-- Constraints for table `student_course`
--
ALTER TABLE `student_course`
  ADD CONSTRAINT `student_course_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `student_course_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
