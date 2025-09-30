# Mapping API actions to their target tables & allowed columns
api_columns = {
    "CREATEUSER": {
        "table": "users",
        "columns": {"name", "email","mobile"}
    },
    "CREATELOG": {
        "table": "m_logs",
        "columns": {"m_snd", "m_reci", "m_api", "m_ip"}
    },
    "LOGINUSER": {
        "table": "users",
        "columns": {"mobile"}
    },
    "GETGOALS": {
        "table": "goals",
        "columns": {"ipadd","userid"}
    },
    "GENERATETXN": {
        "table": "upitxn",
        "columns": {"uid","amt","type","name","jsp"}
    },
    "GETTXN": {
        "table": "report",
        "columns": {"uid"}
    },
    "CREATEGOAL": {
        "table": "usr_goals",
        "columns": {"uid", "goal_id", "goal_amt", "saving_type",
                     "group_saving", "other_details"}
    },
    "JOINGOAL": {
        "table": "usr_goals",
        "columns": {"uid", "goal_id", "goal_amt", "saving_type",
                     "group_saving", "other_details"}
    },
    "CONTRIBUTORS": {
        "table": "goal_contributors",
        "columns": {"uid"}
    },
    "GETGOAL": {
        "table": "usr_goals",
        "columns": {"id"}
    },
    "JOINGOAL": {   
        "table": "goal_contributors",
        "columns": {"goal_db_id", "uid","paid_amt","share_amt"}
    },
    "CHECKALREADYJOIN": {   
        "table": "goal_contributors",
        "columns": {"goal_db_id", "uid"}
    },
    "GOALCALCULATION": {   
        "table": "goal_contributors",
        "columns": {"goal_db_id", "uid"}
    },

}
def validate_api(api: str, columns: dict[str, any]):
    """Validate API action, table and columns"""
    if api not in api_columns:
        raise ValueError(f"Invalid API action: {api}")
    
    table_info = api_columns[api]
    table, allowed = table_info["table"], table_info["columns"]
    extra_columns = set(columns) - allowed
    if extra_columns:
        raise ValueError(f"Parameter(s) extra/not allowed: {extra_columns}")

    missing_col = allowed - set(columns)
    if missing_col:
        raise ValueError(f"Missing Parameter: {missing_col}")
    
    safe_columns = [col for col in columns if col in allowed]

    return table, safe_columns
