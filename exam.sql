-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-03-17 22:05:45
-- 服务器版本： 8.0.12
-- PHP 版本： 7.2.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `exam`
--

-- --------------------------------------------------------

--
-- 表的结构 `match_info`
--

CREATE TABLE `match_info` (
  `match_start_time` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `match_end_time` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0',
  `match_duration` int(11) NOT NULL DEFAULT '0',
  `match_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT ' ',
  `one_question_score` int(11) NOT NULL DEFAULT '0',
  `once_exam_nums` int(10) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `match_info`
--

INSERT INTO `match_info` (`match_start_time`, `match_end_time`, `match_duration`, `match_name`, `one_question_score`, `once_exam_nums`) VALUES
('2020-03-15T00:00', '2020-03-19T00:00', 5, '假装这是一个比赛', 20, 5);

-- --------------------------------------------------------

--
-- 表的结构 `questions`
--

CREATE TABLE `questions` (
  `description` text NOT NULL,
  `answerA` text NOT NULL,
  `answerB` text NOT NULL,
  `answerC` text NOT NULL,
  `answerD` text NOT NULL,
  `answer` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `questions`
--

INSERT INTO `questions` (`description`, `answerA`, `answerB`, `answerC`, `answerD`, `answer`, `id`) VALUES
('关键路径是事件节点网络中（）', '从源点到汇点的最长路径', '从源点到汇点的最短路径', '最长的回路', '最短的回路', 'B', 87),
('任何一个无向图的最小生成树（）', '只有一棵', '有一棵或者多棵', '一定有多棵', '可能不存在', 'B', 88),
('下列排序方法中，哪一种方法的比较次数与记录的初始排列状态无关？', '直接插入排序', '气泡排序', '快速排序', '直接选择排序', 'C', 90),
('n 个顶点的强连通图至少有（）条边', 'n', 'n+1', 'n-1', 'n(n-1)', 'A', 86),
('中序遍历的顺序是（）', '根节点、左子树、右子树', '左子树、根节点、右子树', '右子树、根节点、左子树', '左子树、右子树、根节点', 'B', 85),
('前序遍历的顺序是（）', '根节点、左子树、右子树', '左子树、根节点、右子树', '右子树、根节点、左子树', '左子树、右子树、根节点', 'A', 84),
('如果节点 A 有 3 个兄弟，而且 B 是 A 的双亲，则 B 的度是（）', '4', '5', '1', '2', 'A', 83),
('已知广义表 LS=(a,(b,c,d),e)，运用 HEAD 和 TAIL 函数取出 LS 中单元素 b 的运算是', 'HEAD（HEAD（LS））', 'TAIL(HEAD(LS))', 'HEAD(HEAD(TAIL(LS)))', 'HEAD(TAIL(LS))', 'C', 82),
('设有一个 10 阶的对称矩阵 A，采用下三角方式压缩存储方式，以行序为主存储，a11 为\r\n第一个元素，其存储地址为 1，每个元素占 1 个地址空间，则 a85 的地址为（）', '13', '33', '18', '40', 'B', 81),
('设有两个串 p 和 q，求 q 在 p 中首次出现的位置的运算是', '连接', '模式匹配', '求字串', '求串长', 'D', 80),
('串的长度是', '串中不同字母的个数', '串中不同字符的个数', '串中所含字符的个数，且大于 0', '串中所含字符的个数', 'D', 79),
('一个栈的输入序列为 1,2,3,4,5，则下列序列中不可能是栈的输出序列的是', '2,3,4,1,5', '5,4,1,3,2', '2,3,1,4,5', '1,5,4,3,2', 'B', 78),
('如果线性表中最常用的操作是存取第 i 个元素及其前驱的值，则采用 存储方式节省\r\n时间', '单链表', '双链表', '单循环链表', '顺序表', 'D', 77),
('下列叙述中，正确的是', '线性表的线性存贮结构优于链表存贮结构', '队列的操作方式是先进后出', '栈的操作方式是先进先出', '二维数组是指它的每个数据元素为一个线性表的线性表', 'D', 76),
('线性表若采用链表存贮结构，要求内存中可用存贮单元地址', '必须连续', '部分地址必须连续', '一定不连续', '连续不连续均可', 'D', 75),
('下面关于算法的错误说法是', '算法必须有输出', '算法必须在计算机上用某种语言实现', '算法不一定有输入', '算法必须在有限步执行后能结束', 'B', 74),
('以下哪一个不是栈的基本运算', '删除栈顶元素', '删除栈底的元素', '判断栈是否为空', '将栈置为空栈', 'B', 73),
('在一个有向图中,所有顶点的入度之和等于所有顶点的出度之和的(   ) 倍', '1/2', '1', '2', '4', 'B', 72),
('一个向量第一个元素的存储地址是100,每个元素的长度是2,则第5个元素的地址是', '110', '108', '100', '109', 'B', 70),
('按照二叉树的定义,具有3个结点的二叉树有(    ) 种', '3', '4', '5', '6', 'C', 71),
('要连通具有n个顶点的有向图,至少需要()条边', 'n-1', 'n', 'n+1', '2n', 'B', 68),
('一棵124个叶结点的完全二叉树,最多有()个结点', '247', '248', '249', '250', 'B', 69);

-- --------------------------------------------------------

--
-- 表的结构 `score`
--

CREATE TABLE `score` (
  `username` varchar(20) NOT NULL,
  `score` int(11) NOT NULL,
  `start_time` varchar(30) NOT NULL,
  `finish_time` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `spend_time` int(30) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `password` varchar(50) NOT NULL,
  `is_admin` int(11) DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `is_admin`) VALUES
(20, 'user3', 'user3@user3.com', 'password3', 0),
(19, 'user2', 'user2@user2.com', 'password2', 0),
(18, 'user1', 'user1@user1.com', 'password1', 0),
(1, 'admin', 'admin@admin.com', 'password', 1);

--
-- 转储表的索引
--

--
-- 表的索引 `match_info`
--
ALTER TABLE `match_info`
  ADD PRIMARY KEY (`match_name`);

--
-- 表的索引 `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `score`
--
ALTER TABLE `score`
  ADD PRIMARY KEY (`username`);

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
