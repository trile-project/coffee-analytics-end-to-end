CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `v_sales_line` AS
    SELECT 
        `t`.`transaction_id` AS `transaction_id`,
        COALESCE(STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                            '',
                            ''),
                        '%Y-%m-%d %H:%i:%s'),
                STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                            '',
                            ''),
                        '%Y-%m-%d %H:%i'),
                STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                            '',
                            ''),
                        '%m/%d/%Y %H:%i:%s'),
                STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                            '',
                            ''),
                        '%m/%d/%Y %H:%i'),
                STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                            '',
                            ''),
                        '%m/%d/%Y %h:%i %p'),
                STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                            '',
                            ''),
                        '%m/%d/%Y %h:%i:%s %p')) AS `transaction_ts_parsed`,
        CAST(COALESCE(STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%Y-%m-%d %H:%i:%s'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%Y-%m-%d %H:%i'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %H:%i:%s'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %H:%i'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %h:%i %p'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %h:%i:%s %p'))
            AS DATE) AS `order_date`,
        HOUR(COALESCE(STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%Y-%m-%d %H:%i:%s'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%Y-%m-%d %H:%i'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %H:%i:%s'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %H:%i'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %h:%i %p'),
                    STR_TO_DATE(REPLACE(TRIM(`t`.`transaction_ts`),
                                '',
                                ''),
                            '%m/%d/%Y %h:%i:%s %p'))) AS `order_hour`,
        DATE_FORMAT(`t`.`transaction_ts`, '%H:%i') AS `order_time`,
        `t`.`store_id` AS `store_id`,
        `s`.`city` AS `city`,
        `s`.`region` AS `region`,
        `s`.`store_type` AS `store_type`,
        `t`.`customer_id` AS `customer_id`,
        `c`.`loyalty_tier` AS `loyalty_tier`,
        `t`.`channel` AS `channel`,
        `t`.`payment_method` AS `payment_method`,
        `t`.`promo_type` AS `promo_type`,
        `t`.`order_wait_sec` AS `order_wait_sec`,
        `t`.`service_time_sec` AS `service_time_sec`,
        `t`.`is_refund` AS `is_refund`,
        `t`.`refund_reason` AS `refund_reason`,
        `t`.`employee_id` AS `employee_id`,
        `e`.`role` AS `employee_role`,
        `i`.`line_nbr` AS `line_nbr`,
        `i`.`product_id` AS `product_id`,
        `p`.`product_name` AS `product_name`,
        `i`.`category` AS `category`,
        `i`.`size` AS `size`,
        `i`.`milk` AS `milk`,
        `i`.`temp` AS `temp`,
        `i`.`addon_shots` AS `addon_shots`,
        `i`.`addon_syrup_pumps` AS `addon_syrup_pumps`,
        `i`.`qty` AS `qty`,
        `i`.`unit_price` AS `unit_price`,
        `i`.`unit_cogs` AS `unit_cogs`,
        `i`.`line_discount` AS `line_discount`,
        (`i`.`qty` * `i`.`unit_price`) AS `line_subtotal`,
        (`i`.`qty` * `i`.`line_discount`) AS `line_discount_total`,
        (`i`.`qty` * (`i`.`unit_price` - `i`.`line_discount`)) AS `line_net_sales`,
        (`i`.`qty` * `i`.`unit_cogs`) AS `line_cogs`,
        ((`i`.`qty` * (`i`.`unit_price` - `i`.`line_discount`)) - (`i`.`qty` * `i`.`unit_cogs`)) AS `line_margin`
    FROM
        (((((`fact_transactions` `t`
        JOIN `fact_transaction_items` `i` ON ((`t`.`transaction_id` = `i`.`transaction_id`)))
        LEFT JOIN `dim_products` `p` ON ((`i`.`product_id` = `p`.`product_id`)))
        LEFT JOIN `dim_stores` `s` ON ((`t`.`store_id` = `s`.`store_id`)))
        LEFT JOIN `dim_customers` `c` ON ((`t`.`customer_id` = `c`.`customer_id`)))
        LEFT JOIN `dim_employees` `e` ON ((`t`.`employee_id` = `e`.`employee_id`)))