"""
Functions relating to managing class features.

NOTE: Do not modify `character` in this file. Treat it like a constant.
If `character` must be changed, then the function should be a method of that class instead.
"""
import logging
from typing import TYPE_CHECKING
from dnd_character.SRD import SRD_class_levels

if TYPE_CHECKING:
    from dnd_character.character import Character

LOG = logging.getLogger(__package__)


def get_class_features_data(character: "Character") -> dict:
    """
    Creates a dict for class features. Assumes a fully rested character!
    """
    class_level = character.level
    class_name = character.class_name
    if class_name is None:
        return None

    # Load level appropriate class features
    data = SRD_class_levels[class_name.lower()][class_level - 1][
        "class_specific"
    ].copy()

    # Create class feature counters
    if class_name == "Barbarian":
        data["max_rage_count"] = data["rage_count"]
        data.pop("rage_count")

    elif class_name == "Bard":
        data["max_inspiration_count"] = max(
            1, character.get_ability_modifier(character.charisma)
        )

    elif class_name == "Cleric":
        data["max_channel_divinity_charges"] = data["channel_divinity_charges"]
        data.pop("channel_divinity_charges")

        data["max_divine_intervention_charges"] = 1 if class_level >= 10 else 0

    elif class_name == "Druid":
        data["max_wild_shape_charges"] = 1 if class_level >= 2 else 0

    elif class_name == "Fighter":
        data["max_action_surges"] = data["action_surges"]
        data.pop("action_surges")

        data["max_indomitable_uses"] = data["indomitable_uses"]
        data.pop("indomitable_uses")

        data["max_second_wind"] = 1
        data["available_second_wind"] = 1

    elif class_name == "Monk":
        data["max_ki_points"] = data["ki_points"]
        data.pop("ki_points")

        data["max_wholeness_of_body"] = 1 if class_level >= 6 else 0

    elif class_name == "Paladin":
        data["max_divine_sense"] = 1 + character.get_ability_modifier(
            character.charisma
        )
        data["max_lay_on_hands_points"] = 5 * class_level
        data["max_channel_divinity"] = 1
        data["max_cleansing_touch"] = max(
            1, character.get_ability_modifier(character.charisma)
        )

    elif class_name == "Ranger":
        pass  # No interaction between class features and rest mechanic

    elif class_name == "Rogue":
        data["max_stroke_of_luck"] = 1 if class_level >= 20 else 0

    elif class_name == "Sorcerer":
        data["max_sorcery_points"] = data["sorcery_points"]
        data.pop("sorcery_points")

    elif class_name == "Warlock":
        data["max_mire_the_mind"] = 1 if class_level >= 5 else 0
        data["max_sign_of_ill_omen"] = 1 if class_level >= 5 else 0
        data["max_dark_one's_own_luck"] = 1 if class_level >= 6 else 0
        data["max_bewitching_whispers"] = 1 if class_level >= 7 else 0
        data["max_dreadful_word"] = 1 if class_level >= 7 else 0
        data["max_sculptor_of_flesh"] = 1 if class_level >= 7 else 0
        data["max_thief_of_five_fates"] = 1 if class_level >= 7 else 0
        data["max_minions_of_chaos"] = 1 if class_level >= 9 else 0
        data["max_fiendish_resilience"] = 1 if class_level >= 10 else 0
        data["max_hurl_through_hell"] = 1 if class_level >= 14 else 0
        data["max_chains_of_carceri"] = 1 if class_level >= 20 else 0
        data["max_eldritch_master"] = 1 if class_level >= 20 else 0

    elif class_name == "Wizard":
        data["max_arcane_recovery"] = 1

    # Assign counters (initialized for a fully rested state)
    data = reset_class_features_data_counters(
        character=character,
        data=data,
        short_rest=True,
        long_rest=True,
        reset_day_counters=True,
    )

    return data


def reset_class_features_data_counters(
    character: "Character",
    data: dict,
    short_rest: bool,
    long_rest: bool,
    reset_day_counters: bool = False,
) -> dict:
    """
    Reset counters for class features that deplete and/or cooldown
    A counter that depletes: barbarian's available_rage_count
    A counter that depletes and has cooldown: cleric's divine intervention
    """
    if not short_rest and not long_rest:
        LOG.warning(
            "Calling `reset_class_features_data_counters` with short_rest and long_short both set to False. This is meaningless."
        )
        return data

    class_name = character.class_name

    if class_name == "Barbarian":
        if long_rest:
            data["available_rage_count"] = data["max_rage_count"]

    elif class_name == "Bard":
        if long_rest or character.level >= 5:
            data["available_inspiration_count"] = data["max_inspiration_count"]

    elif class_name == "Cleric":
        if long_rest:
            data["available_divine_intervention_charges"] = data[
                "max_divine_intervention_charges"
            ]
        data["available_channel_divinity_charges"] = data[
            "max_channel_divinity_charges"
        ]
        if reset_day_counters:
            # TODO implement 7 day cooldown
            data["days_since_last_divine_intervention"] = 999

    elif class_name == "Druid":
        data["available_wild_shape_charges"] = data["max_wild_shape_charges"]

    elif class_name == "Fighter":
        data["available_action_surges"] = data["max_action_surges"]
        data["available_indomitable_uses"] = data["max_indomitable_uses"]
        data["available_second_wind"] = 1

    elif class_name == "Monk":
        if long_rest:
            data["available_wholeness_of_body"] = data["max_wholeness_of_body"]
        data["available_ki_points"] = data["max_ki_points"]

    elif class_name == "Paladin":
        if long_rest:
            data["available_divine_sense"] = data["max_divine_sense"]
            data["available_lay_on_hands_points"] = data["max_lay_on_hands_points"]
            data["available_cleansing_touch"] = data["max_cleansing_touch"]
        data["available_channel_divinity"] = 1

    elif class_name == "Ranger":
        pass  # No interaction between class features and rest mechanic

    elif class_name == "Rogue":
        data["available_stroke_of_luck"] = data["max_stroke_of_luck"]

    elif class_name == "Sorcerer":
        if long_rest:
            data["available_sorcery_points"] = data["max_sorcery_points"]

    elif class_name == "Warlock":
        if long_rest:
            data["available_mire_the_mind"] = data["max_mire_the_mind"]
            data["available_sign_of_ill_omen"] = data["max_sign_of_ill_omen"]
            data["available_dark_one's_own_luck"] = data["max_dark_one's_own_luck"]
            data["available_bewitching_whispers"] = data["max_bewitching_whispers"]
            data["available_dreadful_word"] = data["max_dreadful_word"]
            data["available_sculptor_of_flesh"] = data["max_sculptor_of_flesh"]
            data["available_thief_of_five_fates"] = data["max_thief_of_five_fates"]
            data["available_minions_of_chaos"] = data["max_minions_of_chaos"]
            data["available_fiendish_resilience"] = data["max_fiendish_resilience"]
            data["available_hurl_through_hell"] = data["max_hurl_through_hell"]
            data["available_chains_of_carceri"] = data["max_chains_of_carceri"]
            data["available_eldritch_master"] = data["max_eldritch_master"]

    elif class_name == "Wizard":
        data["available_arcane_recovery"] = data["max_arcane_recovery"]
        if reset_day_counters:
            # TODO implement 1 day cooldown
            data["days_since_last_arcane_recovery"] = 999

    return data
