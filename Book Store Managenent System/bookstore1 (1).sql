-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 28, 2025 at 05:37 AM
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
-- Database: `bookstore1`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `first_name`, `password`) VALUES
(1, 'Jay', '1881');

-- --------------------------------------------------------

--
-- Table structure for table `bill`
--

CREATE TABLE `bill` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `order_date` datetime DEFAULT current_timestamp(),
  `book_category` varchar(255) DEFAULT NULL,
  `book_name` varchar(255) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `name`, `category`, `quantity`, `price`) VALUES
(1, 'Anthropology', 'Social Science', 10, 350.00),
(2, 'Economics', 'Social Science', 17, 400.00),
(3, 'Political', 'Social Science', 8, 400.00),
(4, 'Psychology', 'Social Science', 10, 480.00),
(5, 'Nda', 'General Knowledge', 10, 200.00),
(6, 'Mahabharata', 'Mythology', 20, 300.00),
(7, 'Ramayana', 'Mythology', 10, 350.00),
(8, 'Jaya', 'Mythology', 13, 380.00),
(9, 'Uttar Pradesh', 'General Knowledge', 10, 300.00),
(10, 'Samanya', 'General Knowledge', 20, 450.00);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  `book_category` varchar(255) DEFAULT NULL,
  `book_name` varchar(255) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `order_date`, `book_category`, `book_name`, `quantity`, `price`, `total_price`) VALUES
(1, 28, '2025-02-27 22:50:45', 'General Knowledge', 'Nda', 2, 200.00, 400.00),
(2, 28, '2025-02-27 23:08:08', 'General Knowledge', 'Nda', 1, 200.00, 200.00),
(3, 32, '2025-02-27 23:35:15', 'General Knowledge', 'NDA', 2, 200.00, 400.00),
(4, 33, '2025-02-28 00:09:36', 'General Knowledge', 'Nda', 2, 200.00, 400.00),
(5, 33, '2025-02-28 00:11:25', 'Mythology', 'Jaya', 1, 380.00, 380.00),
(6, 35, '2025-02-28 09:38:11', 'General Knowledge', 'Samanya', 2, 450.00, 900.00),
(7, 29, '2025-02-28 10:00:32', 'General Knowledge', 'Nda', 1, 200.00, 200.00),
(8, 29, '2025-02-28 10:00:47', 'Mythology', 'Jaya', 4, 380.00, 1520.00),
(9, 25, '2025-02-28 10:02:19', 'Social Science', 'Psychology', 2, 480.00, 960.00),
(10, 25, '2025-02-28 10:02:41', 'Social Science', 'Political', 1, 400.00, 400.00);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `phone_number` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `first_name`, `phone_number`) VALUES
(22, 'Rushil', '+919104173474'),
(23, 'Charvin', '+917859982654'),
(24, 'Harshil', '+919054291325'),
(25, 'Sujal', '+917984241296'),
(26, 'Kavya', '+919903703730'),
(27, 'Aayush', '+918469725487'),
(28, 'kavyaben vatiya', '+919913703730'),
(29, 'Sahil', '+918160764078'),
(30, 'Dhruv', '+917817879921'),
(31, 'jay', '+918238028070'),
(32, 'KAVY', '9913703730'),
(33, 'Prince', '+919909688582'),
(34, 'Keval', '7046539622'),
(35, 'keval', '+917046539622'),
(36, 'Sujal', '+917984241296'),
(37, 'sahil', '+918160764078');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `first_name` (`first_name`);

--
-- Indexes for table `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `bill`
--
ALTER TABLE `bill`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bill`
--
ALTER TABLE `bill`
  ADD CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
