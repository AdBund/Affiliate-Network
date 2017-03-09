class CreateStatistic < ActiveRecord::Migration[5.0]
  def change
    create_table :statistics do |t|
      t.string :carriers
      t.string :category
      t.string :countries
      t.string :conversion_flow
      t.string :exclusive
      t.string :offer_type
      t.string :payout
      t.text :preview_url
      t.text :offer_description
      t.string :tracklink
      t.date :date

      t.belongs_to :provider, index: true, foreign_key: {on_delete: :nullify}
      t.belongs_to :affiliate, index: true, foreign_key: {on_delete: :nullify}
      t.belongs_to :api_token, index: true, foreign_key: {on_delete: :nullify}

      t.index [:affiliate_id, :tracklink, :payout, :conversion_flow, :offer_type, :provider_id, :api_token_id], unique: true, name: "unique_daily_report"
    end
  end
end
