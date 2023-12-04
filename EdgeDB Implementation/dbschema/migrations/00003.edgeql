CREATE MIGRATION m1hhhld5rn3jiclm4dmageq2nfeeglpzfjwaaxaed27pzlvrlhhhbq
    ONTO m1nb2yvirzlvdbs53w3raaba57lbj723qii6wz3pj5rrs4pwqjp3cq
{
  ALTER TYPE default::Notes {
      DROP CONSTRAINT std::exclusive ON ((.name, .belongs_to));
  };
  ALTER TYPE default::Notes {
      CREATE CONSTRAINT std::exclusive ON (.name);
  };
  ALTER TYPE default::ScentGroup {
      DROP LINK has_notes;
  };
  ALTER TYPE default::Notes {
      DROP LINK belongs_to;
  };
};
