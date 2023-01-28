Method1: UPDATE seats SET owner = 'X' WHERE id = 14 AND is_booked = 0;

Method2: SELECT * FROM seats WHERE id = 14 AND is_booked = 0 FOR UPDATE;
