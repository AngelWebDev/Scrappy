<template>
  <v-card>
    <v-card-title>
      <span class="headline">{{
        $t(`form-data.${formTitle.toLowerCase()}`)
      }}</span>
    </v-card-title>

    <v-card-text>
      <v-container>
        <v-row>
          <v-col cols="6"></v-col>
          <v-col cols="6" class="text-left">
            <h3>{{ $t("form-data.access-rights") }}</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6" md="6">
            <v-text-field
              v-model="editedItem.email"
              label="Email"
            ></v-text-field>
            <v-text-field
              v-model="editedItem.name"
              :label="$t('table-data.fullname')"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-checkbox
              v-model="editedItem.arrival"
              :label="$t('table-data.arrival')"
            ></v-checkbox>
            <v-checkbox
              v-model="editedItem.payout"
              :label="$t('table-data.payout')"
            ></v-checkbox>
            <v-checkbox
              v-model="editedItem.office"
              :label="$t('table-data.office')"
            ></v-checkbox>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="red darken-1" text @click="close">
        {{ $t("form-data.cancel") }}
      </v-btn>
      <v-btn color="blue darken-1" text @click="invite">
        {{ $t("form-data.invite") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "customer-form",
};
</script>

<style></style>
