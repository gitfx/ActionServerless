require 'json'

# GET /test/result/ruby.json
languages = { en: "English", others: { fr: "Franch", sp: "Spanish"} }
puts JSON.dump languages

# GET /test/result/ruby_second.json
puts JSON.dump languages

# PUT /test/result/ruby_third.json
puts JSON.dump languages
