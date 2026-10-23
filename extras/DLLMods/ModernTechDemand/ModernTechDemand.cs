using System;
using System.Collections.Generic;
using UnityEngine;

// Optional companion to the ModernTech data mod: new markets start small and grow.
// Each listed category starts at 25% of the Popularity set in its TyD file when it
// unlocks, then eases up to 100% over the number of years below and stays there.
public class ModernTechDemandMeta : ModMeta
{
	public override string Name => "ModernTech Demand";

	public override void ConstructOptionsScreen(RectTransform parent, bool inGame)
	{
	}
}

public class ModernTechDemand : ModBehaviour
{
	// "Software type/Category" -> years until demand is fully grown
	private static readonly Dictionary<string, float> GrowthYears = new Dictionary<string, float>
	{
		{ "AI Assistant/Voice assistant", 5 },
		{ "AI Assistant/Chat assistant", 4 },
		{ "AI Assistant/Personal agent", 6 },
		{ "Image Generator/Photo filter app", 3 },
		{ "Image Generator/Text-to-image", 4 },
		{ "Image Generator/Text-to-video", 5 },
		{ "Coding Assistant/Smart autocomplete", 4 },
		{ "Coding Assistant/AI pair programmer", 4 },
		{ "Coding Assistant/Coding agent", 5 },
		{ "Self-Driving Software/Driver assistance", 8 },
		{ "Self-Driving Software/Robotaxi", 12 },
		{ "Social App/Social network", 6 },
		{ "Social App/Photo sharing", 4 },
		{ "Social App/Short video", 4 },
		{ "Messaging App/Instant messenger", 5 },
		{ "Messaging App/Mobile messenger", 5 },
		{ "Mobile Wallet/Mobile banking", 6 },
		{ "Mobile Wallet/Tap to pay", 6 },
		{ "Fitness App/Step tracker", 4 },
		{ "Fitness App/Health coach", 5 },
		{ "Graphics Card/3D accelerator", 3 },
		{ "Graphics Card/Gaming GPU", 5 },
		{ "Graphics Card/AI accelerator", 7 },
		{ "Processor/Desktop CPU", 6 },
		{ "Processor/Server CPU", 5 },
		{ "Processor/Mobile chip", 5 },
	};

	// Popularity from the TyD files, remembered the first time each category is seen
	private readonly Dictionary<SoftwareCategory, float> _fullPopularity = new Dictionary<SoftwareCategory, float>();

	private MarketSimulation _appliedTo;

	public override void OnActivate()
	{
		TimeOfDay.OnMonthPassed += OnMonthPassed;
		Apply();
	}

	public override void OnDeactivate()
	{
		TimeOfDay.OnMonthPassed -= OnMonthPassed;
		foreach (KeyValuePair<SoftwareCategory, float> pair in _fullPopularity)
		{
			pair.Key.Popularity = pair.Value;
		}
		_appliedTo = null;
	}

	private void Update()
	{
		// A new or loaded game has its own market; update it right away instead of next month
		if (MarketSimulation.Active != _appliedTo)
		{
			Apply();
		}
	}

	private void OnMonthPassed(object sender, EventArgs e)
	{
		Apply();
	}

	private void Apply()
	{
		MarketSimulation sim = MarketSimulation.Active;
		_appliedTo = sim;
		if (sim == null || TimeOfDay.Instance == null)
		{
			return;
		}
		float now = SDateTime.Now().ToFloat() + 1900f;
		foreach (SoftwareType type in sim.SoftwareTypes.Values)
		{
			foreach (SoftwareCategory cat in type.Categories.Values)
			{
				float years;
				if (!cat.Unlock.HasValue || !GrowthYears.TryGetValue(type.Name + "/" + cat.Name, out years))
				{
					continue;
				}
				float full;
				if (!_fullPopularity.TryGetValue(cat, out full))
				{
					full = cat.Popularity;
					_fullPopularity[cat] = full;
				}
				cat.Popularity = full * Growth(now - cat.Unlock.Value, years);
			}
		}
	}

	public static float Growth(float age, float years)
	{
		float t = Mathf.Clamp01(age / years);
		return 0.25f + 0.75f * t * t * (3f - 2f * t);
	}
}
