
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(80) NOT NULL,
  `admin` boolean NOT NULL,
  `password` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `users` (`id`, `username`, `admin`, `password`) VALUES
(1, 'tyler9x', 1, 'admin10!'),
(2, 'purple', 0, 'color3711'),
(3, 'yellow', 0, 'buck2344'),
(4, 'pink', 0, 'smiff3548');
