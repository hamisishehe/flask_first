-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2025 at 09:39 AM
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
(1, 'LG 102', 'Communicat', 1, 1, 1, 0, 4, 3),
(2, 'CP 111', 'Principles', 1, 1, 1, 1, 5, 5),
(3, 'DS 102', 'Developmen', 1, 1, 1, 0, 4, 3),
(4, 'IT 111', 'Introducti', 1, 1, 1, 0, 5, 5),
(5, 'TN 112', 'Linear Alg', 1, 1, 1, 0, 5, 5),
(6, 'TN 111', 'Discrete M', 1, 1, 1, 0, 5, 5),
(7, 'IA 112', 'Mathematic', 1, 1, 1, 0, 5, 5),
(8, 'TN 113', 'Calculus', 1, 1, 1, 0, 5, 5),
(16, 'IA 417', 'Cyber Thre', 1, 1, 1, 1, 5, 5),
(17, 'CG 221', 'Fundamenta', 1, 1, 1, 1, 5, 5),
(18, 'CT 411', 'Embedded S', 1, 1, 1, 1, 5, 5),
(19, 'CT 412', 'Parallel C', 1, 1, 1, 1, 5, 5),
(20, 'TN 412', 'Digital Si', 1, 1, 1, 0, 5, 5),
(21, 'CG 411', 'Computer E', 1, 1, 1, 0, 5, 5),
(22, 'CT 413', 'Operating ', 1, 1, 1, 0, 5, 5),
(23, 'IA 314', 'Biometric ', 1, 1, 1, 0, 5, 5),
(24, 'CS 431', 'Software E', 1, 1, 1, 0, 5, 5),
(25, 'CT 312', 'Computer M', 1, 1, 1, 1, 5, 5),
(26, 'IM 411', 'Human-Comp', 1, 1, 1, 0, 5, 5),
(27, 'CP 412', 'C sharp Pr', 1, 1, 1, 1, 5, 5),
(28, 'CS 411', 'Software R', 1, 1, 1, 0, 5, 5),
(29, 'BT 312', 'Electronic', 1, 1, 1, 0, 5, 5),
(30, 'CD 312', 'Multimedia', 1, 1, 1, 0, 4, 3),
(31, 'CP 314', 'Distribute', 1, 1, 1, 0, 5, 5),
(32, 'TN 411', 'Mobile Com', 1, 1, 1, 0, 5, 5),
(33, 'TN 413', 'Informatio', 1, 1, 1, 0, 5, 5),
(34, 'TN 431', 'Telecommun', 1, 1, 1, 0, 5, 5),
(35, 'IA 311', 'Network Fo', 1, 1, 1, 0, 5, 5),
(36, 'CD 431', 'Content En', 1, 1, 1, 0, 4, 3),
(37, 'CD 411', 'Project St', 1, 1, 1, 0, 4, 3),
(38, 'CD 412', 'Video and ', 1, 1, 1, 1, 4, 3),
(39, 'IM 411', 'Human Comp', 1, 1, 1, 0, 4, 3),
(40, 'SI 312', 'Organizati', 1, 1, 1, 0, 4, 3),
(41, 'LW 4110', 'Legal Aspe', 1, 1, 1, 0, 5, 5),
(42, 'IA 418', 'Cyber Crim', 1, 1, 1, 0, 5, 5),
(43, 'CS 418', 'Cyber Secu', 1, 1, 1, 0, 5, 5),
(44, 'LW 4110', 'Legal Aspe', 1, 1, 1, 0, 5, 5),
(47, 'AF 111', 'Introducti', 1, 1, 1, 0, 4, 3),
(48, 'MG 111', 'Principles', 1, 1, 1, 0, 4, 3),
(54, 'CD 112', 'Foundation', 1, 1, 1, 0, 4, 3),
(63, 'CD 111', 'Digital Me', 1, 1, 1, 0, 4, 3),
(72, 'EC 111', 'Fundamenta', 1, 1, 1, 1, 5, 5),
(78, 'CD 113', 'Fundamenta', 1, 1, 1, 1, 4, 3),
(79, 'CN 111', 'Fundamenta', 1, 1, 1, 1, 5, 5),
(80, 'CD 111', 'Digital Me', 1, 1, 1, 0, 4, 3),
(81, 'EME 314', 'ICT Entrep', 1, 1, 1, 0, 4, 3),
(82, 'S1 311', 'Profession', 1, 1, 1, 0, 4, 3),
(83, 'BT 413', 'ICT Projec', 1, 1, 1, 0, 4, 3),
(85, 'Development PerspectGGGGGGGGGGGGGGG', 'CP 555', 1, 1, 1, 0, 4, 3),
(86, 'GGGGGG GGGGGGGGGGGGGGG', 'CP 666', 1, 1, 1, 0, 4, 3);

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
(88, 19, 1, 15, ''),
(89, 19, 1, 21, ''),
(90, 19, 1, 24, ''),
(91, 19, 1, 27, ''),
(92, 19, 1, 34, ''),
(93, 19, 1, 38, ''),
(94, 19, 1, 42, ''),
(95, 19, 1, 46, ''),
(96, 16, 3, 15, ''),
(97, 16, 3, 21, ''),
(98, 16, 3, 24, ''),
(99, 16, 3, 27, ''),
(100, 16, 3, 31, ''),
(101, 16, 3, 34, ''),
(102, 16, 3, 38, ''),
(103, 16, 3, 42, ''),
(104, 16, 3, 46, ''),
(105, 89, 48, 15, ''),
(106, 17, 81, 17, 'A'),
(107, 17, 81, 23, 'A'),
(108, 17, 81, 26, 'A'),
(109, 18, 81, 44, 'B'),
(110, 18, 81, 40, 'B'),
(111, 18, 81, 37, 'B'),
(112, 77, 6, 15, 'A'),
(113, 77, 6, 24, 'A'),
(114, 77, 6, 46, 'A'),
(115, 15, 6, 27, 'B'),
(116, 15, 6, 31, 'B'),
(117, 15, 6, 38, 'B'),
(118, 15, 6, 42, 'B'),
(119, 15, 6, 34, 'B'),
(120, 15, 7, 27, ''),
(121, 15, 7, 31, ''),
(122, 17, 85, 15, ''),
(123, 97, 86, 29, '');

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
(104, 'Leyla', 'leyla', 'layla', 'FEMALE', '777676767', 'leyla@udom.co.tz', 'Mrs', 5, 5);

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
  `programme_code` varchar(100) NOT NULL,
  `total_students` varchar(11) DEFAULT NULL,
  `coordinator_id` int(11) NOT NULL,
  `department_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `programme`, `programme_code`, `total_students`, `coordinator_id`, `department_id`) VALUES
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
(2, 'coordinator', 'A.', 'coordinator', '1234567890', 'coordinator@udom.co.tz', '', 'scrypt:32768:8:1$EGl4tNpQU70d2evf$e91f38fb3b2082edfcb6376872aa5c6b11b36c6dffd46ae84434f060eff727e011366f6ec19b2ffa1ccac5811ad364f11369bcf2f5ec3bdb974e7e006a865a8c', 'COORDINATOR'),
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `course_matrix`
--
ALTER TABLE `course_matrix`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=124;

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
