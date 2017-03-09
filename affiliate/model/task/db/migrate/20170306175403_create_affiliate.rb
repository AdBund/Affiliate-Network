class CreateAffiliate < ActiveRecord::Migration[5.0]
  def change
    create_table :affiliates do |t|
      t.string :affiliate_identity, null: false
      t.string :name
      t.belongs_to :api_token, index: true, foreign_key: {on_delete: :nullify}
      t.belongs_to :provider, index: true, foreign_key: {on_delete: :nullify}
      t.index [:provider_id, :affiliate_identity, :api_token_id], unique: true, name: 'unique_affiliate'
    end
  end
end
