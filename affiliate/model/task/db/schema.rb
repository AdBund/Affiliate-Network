# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20170306181740) do

  create_table "affiliates", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string  "affiliate_identity", null: false
    t.string  "name"
    t.integer "api_token_id"
    t.integer "provider_id"
    t.index ["api_token_id"], name: "index_affiliates_on_api_token_id", using: :btree
    t.index ["provider_id", "affiliate_identity", "api_token_id"], name: "unique_affiliate", unique: true, using: :btree
    t.index ["provider_id"], name: "index_affiliates_on_provider_id", using: :btree
  end

  create_table "api_tokens", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string  "token",       null: false
    t.string  "userId",      null: false
    t.string  "username"
    t.string  "password"
    t.integer "provider_id"
    t.index ["provider_id", "token", "userId", "username", "password"], name: "unique_provider_token", unique: true, using: :btree
    t.index ["provider_id"], name: "index_api_tokens_on_provider_id", using: :btree
    t.index ["token"], name: "index_api_tokens_on_token", using: :btree
  end

  create_table "providers", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string "name", null: false
    t.index ["name"], name: "index_providers_on_name", unique: true, using: :btree
  end

  create_table "statistics", force: :cascade, options: "ENGINE=InnoDB DEFAULT CHARSET=utf8" do |t|
    t.string  "carriers"
    t.string  "category"
    t.string  "countries"
    t.string  "conversion_flow"
    t.string  "exclusive"
    t.string  "offer_type"
    t.string  "payout"
    t.text    "preview_url",       limit: 65535
    t.text    "offer_description", limit: 65535
    t.string  "tracklink"
    t.date    "date"
    t.integer "provider_id"
    t.integer "affiliate_id"
    t.integer "api_token_id"
    t.index ["affiliate_id", "tracklink", "payout", "conversion_flow", "offer_type", "provider_id", "api_token_id"], name: "unique_daily_report", unique: true, using: :btree
    t.index ["affiliate_id"], name: "index_statistics_on_affiliate_id", using: :btree
    t.index ["api_token_id"], name: "index_statistics_on_api_token_id", using: :btree
    t.index ["provider_id"], name: "index_statistics_on_provider_id", using: :btree
  end

  add_foreign_key "affiliates", "api_tokens", on_delete: :nullify
  add_foreign_key "affiliates", "providers", on_delete: :nullify
  add_foreign_key "api_tokens", "providers", on_delete: :nullify
  add_foreign_key "statistics", "affiliates", on_delete: :nullify
  add_foreign_key "statistics", "api_tokens", on_delete: :nullify
  add_foreign_key "statistics", "providers", on_delete: :nullify
end
