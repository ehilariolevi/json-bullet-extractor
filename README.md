# Levi JSON Bullet Extractor

A Streamlit app that extracts Shopify Rich Text bullet content from the `fit_description` field and converts it into structured columns.

## Input File Requirements

Upload an Excel (.xlsx) file containing the following columns:

| Column |
|----------|
| PC-9 |
| PC9 |
| ID |
| Handle |
| fit_description |

## Output Columns

The app generates the following columns:

```text
PC-9
PC9
ID
Handle
Bullet_1
Bullet_2
Bullet_3
Bullet_4
Bullet_5
Bullet_6
Bullet_7
Bullet_8
Model_Info
```

## Extraction Logic

- Extracts Rich Text list items from Shopify JSON
- Populates Bullet_1 through Bullet_8
- If the last bullet begins with "Model", it is moved to the Model_Info column
- Supports up to 8 bullet columns
- Invalid JSON is retained in the output row, with extracted columns left blank

## Example

Input bullets:

```text
Button closure
Slim fit
Stretch denim
Model is 5'10" wearing size 32
```

Output:

```text
Bullet_1 = Button closure
Bullet_2 = Slim fit
Bullet_3 = Stretch denim
Model_Info = Model is 5'10" wearing size 32
```

## Built With

- Streamlit
- Pandas
- OpenPyXL
- Python
