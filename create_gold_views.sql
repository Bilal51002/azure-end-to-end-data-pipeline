USE gold_db
GO

CREATE OR ALTER PROC CreateSQLServerlessView_gold @ViewName nvarchar(100)
AS
BEGIN
    DECLARE @statement VARCHAR(MAX)
    SET @statement = N'CREATE OR ALTER VIEW ' + @ViewName + ' AS
        SELECT
            *
        FROM
            OPENROWSET(
                BULK ''https://intechsg202608.dfs.core.windows.net/gold/SalesLT/' + @ViewName + '/'',
                FORMAT = ''DELTA''
            ) AS [result]'

    EXEC (@statement)
END
GO

-- Appel de la procédure pour chaque table du dossier gold/SalesLT/
EXEC CreateSQLServerlessView_gold 'Address'
EXEC CreateSQLServerlessView_gold 'Customer'
EXEC CreateSQLServerlessView_gold 'CustomerAddress'
EXEC CreateSQLServerlessView_gold 'Product'
EXEC CreateSQLServerlessView_gold 'ProductCategory'
EXEC CreateSQLServerlessView_gold 'ProductDescription'
EXEC CreateSQLServerlessView_gold 'ProductModel'
EXEC CreateSQLServerlessView_gold 'ProductModelProductDescription'
EXEC CreateSQLServerlessView_gold 'SalesOrderDetail'
EXEC CreateSQLServerlessView_gold 'SalesOrderHeader'
GO

-- Vérification : lister les vues créées
SELECT * FROM INFORMATION_SCHEMA.VIEWS