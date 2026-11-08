@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Name prefix for the storage account (3-11 lowercase letters or digits)')
@minLength(3)
@maxLength(11)
param namePrefix string = 'homesense'

@description('Name of the blob container that stores the sensor readings')
param containerName string = 'readings'

var storageAccountName = '${namePrefix}${uniqueString(resourceGroup().id)}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storageAccount
  name: 'default'
}

resource readingsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobService
  name: containerName
  properties: {
    publicAccess: 'None'
  }
}

output storageAccountName string = storageAccount.name
output containerName string = readingsContainer.name
