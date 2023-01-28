package main

import (
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type ReplStat struct {
	Usename         string
	ApplicationName string
	SyncState       string
}

func main() {
	dsn := "host=localhost user=postgres password=postgres dbname=postgres port=5432 sslmode=disable"
	db, _ := gorm.Open(postgres.Open(dsn), &gorm.Config{})

	sqlDB, _ := db.DB()

	var rs ReplStat

	db.Table("pg_stat_replication").Select("usename", "application_name", "sync_state").Scan(&rs)

	sqlDB.Close()

	fmt.Printf("result: %v\n", rs)
}
