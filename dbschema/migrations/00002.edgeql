CREATE MIGRATION m1nb2yvirzlvdbs53w3raaba57lbj723qii6wz3pj5rrs4pwqjp3cq
    ONTO m14zbetimchghp2ugy4e4wiuatnku4nmczhj3hz5cxsukzfqfffmwa
{
  ALTER TYPE default::Review {
      DROP CONSTRAINT std::exclusive ON (.content);
  };
};
