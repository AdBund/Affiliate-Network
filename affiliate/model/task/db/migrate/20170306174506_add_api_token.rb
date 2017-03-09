class AddApiToken < ActiveRecord::Migration[5.0]
  def change
    create_table :providers do |t|
        t.string :name, null: false
        t.index [:name], unique: true
    end

    create_table :api_tokens do |t|
      t.string :token, null:false, index:true
      t.string :userId, null: false
      t.string :username
      t.string :password
      t.belongs_to :provider, index: true, foreign_key: {on_delete: :nullify}
      t.index [:provider_id, :token, :userId, :username, :password], unique: true, name: 'unique_provider_token'
    end
  end
end