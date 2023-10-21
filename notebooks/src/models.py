import tensorflow as tf


class AEFineTuningModel(tf.keras.Model):
    def __init__(
            self,
            bert_model_1,
            bert_model_2,
            num_classes,
            dropout_rate=0.1
    ):
        super(AEFineTuningModel, self).__init__()
        self.bert_model_1 = bert_model_1
        self.bert_model_2 = bert_model_2
        self.concat = tf.keras.layers.Concatenate()
        self.dropout = tf.keras.layers.Dropout(dropout_rate)
        self.classifier = tf.keras.layers.Dense(
            num_classes,
            activation='softmax'
        )

    def call(self, inputs):
        input_ids, token_type_ids, attention_mask = inputs

        output_1 = self.bert_model_1(
            [input_ids, token_type_ids, attention_mask]
        )
        output_2 = self.bert_model_2(
            [input_ids, token_type_ids, attention_mask]
        )

        # Combina as saídas dos dois modelos
        concatenated = self.concat([
            output_1['last_hidden_state'],
            output_2['last_hidden_state']
        ])

        # Adiciona a camada de dropout
        concatenated_dropped = self.dropout(concatenated)

        # Alimenta a camada de classificação
        logits = self.classifier(concatenated_dropped)

        return logits
