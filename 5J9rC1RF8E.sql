-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: remotemysql.com
-- Gegenereerd op: 27 mei 2021 om 13:10
-- Serverversie: 8.0.13-4
-- PHP-versie: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `5J9rC1RF8E`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `accounts`
--

CREATE TABLE `accounts` (
  `iban` varchar(18) NOT NULL,
  `customerID` int(11) NOT NULL,
  `balance` double NOT NULL,
  `cardID` int(11) DEFAULT NULL,
  `typeOfAccount` enum('type1','type2') DEFAULT NULL,
  `login` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `accounts`
--

INSERT INTO `accounts` (`iban`, `customerID`, `balance`, `cardID`, `typeOfAccount`, `login`) VALUES
('NI99ABNA01234567', 2, 1640.3999999999996, 0, 'type1', 1),
('NI99ABNA14789632', 1, 11000, 1, 'type1', 0),
('NI99ABNA20011306', 3, 100, 2, 'type1', 0),
('NI99ABNA69050802', 0, 750, 3, 'type1', 0);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `card`
--

CREATE TABLE `card` (
  `cardID` int(11) NOT NULL,
  `pinCode` varchar(64) NOT NULL,
  `cardUID` varchar(8) NOT NULL,
  `noOfTries` int(11) DEFAULT '0',
  `valid` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `card`
--

INSERT INTO `card` (`cardID`, `pinCode`, `cardUID`, `noOfTries`, `valid`) VALUES
(0, '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'AB34CD24', 0, 1),
(1, '0bf366a6fdd643807e24b567a94e9ab1f24ef87d9353b3248e2bc42503766275', '000', 0, 1),
(2, 'f89328f7804b950087f0fabde05183a45be91aaca59f8d029bb1932bfbc87bc7', 'B6E1162B', 0, 1),
(3, 'dae0392f93b4c0fea31dbfce2bc0173a3d76e9c58e6e391ed4985dc39040b7bf', '12C4C434', 0, 1);

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `customer`
--

CREATE TABLE `customer` (
  `customerID` int(11) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `prefix` varchar(45) DEFAULT NULL,
  `lastName` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zipCode` varchar(6) NOT NULL,
  `country` varchar(255) NOT NULL,
  `e-mail` varchar(255) NOT NULL,
  `phoneNumber` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `customer`
--

INSERT INTO `customer` (`customerID`, `firstName`, `prefix`, `lastName`, `address`, `city`, `zipCode`, `country`, `e-mail`, `phoneNumber`) VALUES
(0, 'Tom', 'van', 'Pelt', 'Glacisweg 49', 'Hellevoetsluis', '3221XA', 'Nederland', '1003212@hr.nl', '0638404353'),
(1, 'Matthijs', NULL, 'Briel', 'Pieter Biggestraat 31', 'Ooltgensplaat', '3257AR', 'Nederland', '0988991@hr.nl', '0620215758'),
(2, 'Leandro', 'de', 'Nijs', 'Tapijtschelp 67', 'Hellevoetsluis', '3225BR', 'Nederland', 'leandrodn10@gmail.com', '0642838590'),
(3, 'Jurre', 'van', 'Wamelen', 'Vleerdamsedijk 12', 'Rockanje', '3235NW', 'Nederland', '1009652@hr.nl', '0625389698'),
(4, 'Arthur', NULL, 'Warren', 'Zonnebloemstraat 29', 'Rotterdam', '3051SW', 'Nederland', 'arthur.warren@example.com', '0623699568'),
(5, 'Sally', NULL, 'Lawrence', 'Heiligerleelaan 17', 'Rotterdam', '3051JJ', 'Nederland', 'S.Lawrence@gmail.com', '0696254996');

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `transactions`
--

CREATE TABLE `transactions` (
  `transactionID` int(11) NOT NULL,
  `transactionType` enum('withdraw','deposit','transfar') NOT NULL,
  `iban` varchar(18) NOT NULL,
  `amount` int(11) DEFAULT NULL,
  `transactionDate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Gegevens worden geëxporteerd voor tabel `users`
--

INSERT INTO `users` (`id`, `user_id`, `user_name`, `password`) VALUES
(3, 123497, 'Jurrevw', '26c6a2a3ce3e1011cc50ee4e117d48fc9b8257b0eac2ccfe449f30b48ae952e6'),
(0, 198745, 'Tomvp', '73c624bf17581ce4935363598b49edcf3a836494a5fd287663faa817cd4b72e8'),
(2, 986373, 'Leandrodn', '688dd0c147c966604a59a5e820f0d6ddeda6a19314a9bbe4b33fa0c41f74c56c'),
(1, 2456098, 'Matthijsb', '0fba89e66b8302306edd9095ef9520a44319a49c4e7ea64b5a36ed204aa832ff');

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`iban`),
  ADD KEY `FK_customerID` (`customerID`),
  ADD KEY `FK_cardID` (`cardID`);

--
-- Indexen voor tabel `card`
--
ALTER TABLE `card`
  ADD PRIMARY KEY (`cardID`);

--
-- Indexen voor tabel `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customerID`);

--
-- Indexen voor tabel `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transactionID`),
  ADD KEY `FK_iban` (`iban`);

--
-- Indexen voor tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `userID` (`id`);

--
-- Beperkingen voor geëxporteerde tabellen
--

--
-- Beperkingen voor tabel `accounts`
--
ALTER TABLE `accounts`
  ADD CONSTRAINT `FK_cardID` FOREIGN KEY (`cardID`) REFERENCES `card` (`cardid`),
  ADD CONSTRAINT `FK_customerID` FOREIGN KEY (`customerID`) REFERENCES `customer` (`customerid`);

--
-- Beperkingen voor tabel `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `FK_iban` FOREIGN KEY (`iban`) REFERENCES `accounts` (`iban`);

--
-- Beperkingen voor tabel `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `userID` FOREIGN KEY (`id`) REFERENCES `customer` (`customerid`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
