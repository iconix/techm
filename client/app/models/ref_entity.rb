class RefEntity < ActiveRecord::Base
  #belongs_to :article

  has_one :entity
end
